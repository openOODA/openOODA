/* tests_c_abi_layout.c — Regression & FFI verification for Devin Items 3 & 5.
 *
 * Validates:
 * 1. repr(C) memory layout contracts for TerminalCell (16B) and GpuCell (24B).
 * 2. Caller-Allocates Callee-Fills out-param grid buffer protocol via oo_ffi_call.
 * 3. 16-byte struct-by-value argument passing under System V AMD64 ABI.
 * 4. Dynamic library loading (dlopen -> dlsym -> ffi_call -> dlclose) round-trip.
 *
 * Complies with RULES.oot <= 256 lines.
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stddef.h>
#include <dlfcn.h>
#include <assert.h>
#include "../../oodar/oodar.h"

/* Layout Contracts per PLUGIN_ABI_SPEC.oot */
typedef struct {
  uint32_t codepoint;
  uint32_t fg;
  uint32_t bg;
  uint32_t attrs;
} TerminalCell;

typedef struct {
  float x;
  float y;
  float u;
  float v;
  uint32_t fg_rgba;
  uint32_t bg_rgba;
} GpuCell;

/* Simulates plugin rendering into caller-supplied grid buffer */
static void dummy_render(TerminalCell *grid, uint32_t width, uint32_t height, uint32_t tick) {
  if (!grid) return;
  for (uint32_t y = 0; y < height; y++) {
    for (uint32_t x = 0; x < width; x++) {
      uint32_t idx = y * width + x;
      grid[idx].codepoint = (uint32_t)('A' + ((idx + tick) % 26));
      grid[idx].fg = 0x00FF00;
      grid[idx].bg = 0x000000;
      grid[idx].attrs = 1;
    }
  }
}

/* Simulates function accepting 16-byte struct by value */
static uint64_t dummy_cell_checksum(TerminalCell cell) {
  return (uint64_t)cell.codepoint + (uint64_t)cell.fg + (uint64_t)cell.bg + (uint64_t)cell.attrs;
}

static int test_repr_c_layout(void) {
  if (sizeof(TerminalCell) != 16 || _Alignof(TerminalCell) != 4) return 1;
  if (offsetof(TerminalCell, codepoint) != 0 || offsetof(TerminalCell, fg) != 4 ||
      offsetof(TerminalCell, bg) != 8 || offsetof(TerminalCell, attrs) != 12) return 1;

  if (sizeof(GpuCell) != 24 || _Alignof(GpuCell) != 4) return 1;
  if (offsetof(GpuCell, x) != 0 || offsetof(GpuCell, y) != 4 ||
      offsetof(GpuCell, u) != 8 || offsetof(GpuCell, v) != 12 ||
      offsetof(GpuCell, fg_rgba) != 16 || offsetof(GpuCell, bg_rgba) != 20) return 1;
  printf("OK\tlayout\tTerminalCell (16B) and GpuCell (24B) repr(C) alignments verified\n");
  return 0;
}

static int test_outparam_render_protocol(long long cap) {
  const uint32_t W = 80;
  const uint32_t H = 25;
  TerminalCell grid[80 * 25];
  memset(grid, 0, sizeof(grid));

  char sym_tok[64];
  snprintf(sym_tok, sizeof(sym_tok), "sym:%p", (void *)(intptr_t)dummy_render);

  char ptr_tok[64];
  snprintf(ptr_tok, sizeof(ptr_tok), "ptr:%p", (void *)grid);

  char argv_buf[256];
  snprintf(argv_buf, sizeof(argv_buf), "%s\t%u\t%u\t%u", ptr_tok, W, H, 10);

  OoResS r = oo_ffi_call(cap, oo_str_lit(sym_tok), oo_str_lit("v"), oo_str_lit("puuu"), oo_str_lit(argv_buf));
  if (!r.ok) {
    fprintf(stderr, "FAIL: oo_ffi_call dummy_render failed: %.*s\n", (int)r.val.len, r.val.data ? r.val.data : "");
    return 1;
  }

  /* Verify grid was populated by dummy_render */
  if (grid[0].codepoint != (uint32_t)('A' + (10 % 26))) {
    fprintf(stderr, "FAIL: grid[0].codepoint = %u, expected %u\n", grid[0].codepoint, (uint32_t)('A' + (10 % 26)));
    return 1;
  }
  if (grid[0].fg != 0x00FF00 || grid[0].attrs != 1) {
    fprintf(stderr, "FAIL: grid[0] attributes corrupted\n");
    return 1;
  }
  if (grid[W * H - 1].codepoint != (uint32_t)('A' + ((W * H - 1 + 10) % 26))) {
    fprintf(stderr, "FAIL: last cell glyph corrupted\n");
    return 1;
  }
  printf("OK\toutparam\tCaller-Allocates Callee-Fills grid buffer protocol verified\n");
  return 0;
}

static int test_struct_by_value(long long cap) {
  TerminalCell c;
  c.codepoint = 65;
  c.fg = 100;
  c.bg = 200;
  c.attrs = 5;

  uint64_t expected_sum = 65 + 100 + 200 + 5;
  uint64_t *halves = (uint64_t *)&c;

  char sym_tok[64];
  snprintf(sym_tok, sizeof(sym_tok), "sym:%p", (void *)(intptr_t)dummy_cell_checksum);

  char argv_buf[128];
  snprintf(argv_buf, sizeof(argv_buf), "%llu\t%llu", (unsigned long long)halves[0], (unsigned long long)halves[1]);

  OoResS r = oo_ffi_call(cap, oo_str_lit(sym_tok), oo_str_lit("l"), oo_str_lit("ll"), oo_str_lit(argv_buf));
  if (!r.ok) {
    fprintf(stderr, "FAIL: oo_ffi_call struct_by_value failed\n");
    return 1;
  }
  uint64_t got = (uint64_t)strtoull(r.val.data, NULL, 10);
  if (got != expected_sum) {
    fprintf(stderr, "FAIL: struct_by_value checksum got %llu, expected %llu\n",
            (unsigned long long)got, (unsigned long long)expected_sum);
    return 1;
  }
  printf("OK\tby_value\t16-byte struct-by-value SysV register decomposition verified\n");
  return 0;
}

static int test_dlopen_roundtrip(long long cap) {
  setenv("OODA_FFI_ALLOW_DLOPEN", "1", 1);
  /* Build a tiny standalone plugin .so */
  const char *plugin_src = "/tmp/test_screensaver_plugin.c";
  const char *plugin_so = "/tmp/test_screensaver_plugin.so";

  FILE *f = fopen(plugin_src, "w");
  if (!f) return 1;
  fprintf(f,
    "#include <stdint.h>\n"
    "typedef struct { uint32_t codepoint, fg, bg, attrs; } TerminalCell;\n"
    "__attribute__((visibility(\"default\"))) uint32_t plugin_api_version(void) { return 1; }\n"
    "__attribute__((visibility(\"default\"))) void *plugin_create(void) { return (void *)(uintptr_t)0xCAFE; }\n"
    "__attribute__((visibility(\"default\"))) void plugin_render(void *s, TerminalCell *g, uint32_t w, uint32_t h) {\n"
    "  if (g && w > 0 && h > 0) { g[0].codepoint = 42; g[0].fg = 0xFF; }\n"
    "}\n"
    "__attribute__((visibility(\"default\"))) void plugin_destroy(void *s) { (void)s; }\n"
  );
  fclose(f);

  char cmd[512];
  snprintf(cmd, sizeof(cmd), "gcc -shared -fPIC -O2 -o %s %s", plugin_so, plugin_src);
  if (system(cmd) != 0) {
    fprintf(stderr, "FAIL: failed to compile test plugin shared library\n");
    return 1;
  }

  /* 1. dlopen */
  void *h = dlopen(plugin_so, RTLD_NOW | RTLD_LOCAL);
  if (!h) {
    fprintf(stderr, "FAIL: dlopen failed: %s\n", dlerror());
    return 1;
  }

  /* 2. dlsym & ffi_call plugin_api_version */
  void *fn_ver = dlsym(h, "plugin_api_version");
  if (!fn_ver) { dlclose(h); return 1; }
  char sym_ver[64];
  snprintf(sym_ver, sizeof(sym_ver), "sym:%p", fn_ver);
  OoResS r_ver = oo_ffi_call(cap, oo_str_lit(sym_ver), oo_str_lit("u"), oo_str_lit(""), oo_str_lit(""));
  if (!r_ver.ok || strcmp(r_ver.val.data, "1") != 0) { dlclose(h); return 1; }

  /* 3. dlsym & ffi_call plugin_create */
  void *fn_create = dlsym(h, "plugin_create");
  if (!fn_create) { dlclose(h); return 1; }
  char sym_create[64];
  snprintf(sym_create, sizeof(sym_create), "sym:%p", fn_create);
  OoResS r_create = oo_ffi_call(cap, oo_str_lit(sym_create), oo_str_lit("p"), oo_str_lit(""), oo_str_lit(""));
  if (!r_create.ok || strncmp(r_create.val.data, "ptr:", 4) != 0) { dlclose(h); return 1; }

  /* 4. dlsym & ffi_call plugin_render */
  TerminalCell host_grid[10];
  memset(host_grid, 0, sizeof(host_grid));
  char grid_tok[64];
  snprintf(grid_tok, sizeof(grid_tok), "ptr:%p", (void *)host_grid);
  char r_args[256];
  snprintf(r_args, sizeof(r_args), "%s\t%s\t10\t1", r_create.val.data, grid_tok);

  void *fn_render = dlsym(h, "plugin_render");
  if (!fn_render) { dlclose(h); return 1; }
  char sym_render[64];
  snprintf(sym_render, sizeof(sym_render), "sym:%p", fn_render);
  OoResS r_rend = oo_ffi_call(cap, oo_str_lit(sym_render), oo_str_lit("v"), oo_str_lit("ppuu"), oo_str_lit(r_args));
  if (!r_rend.ok || host_grid[0].codepoint != 42 || host_grid[0].fg != 0xFF) { dlclose(h); return 1; }

  /* 5. dlsym & ffi_call plugin_destroy */
  void *fn_destroy = dlsym(h, "plugin_destroy");
  if (!fn_destroy) { dlclose(h); return 1; }
  char sym_destroy[64];
  snprintf(sym_destroy, sizeof(sym_destroy), "sym:%p", fn_destroy);
  OoResS r_dest = oo_ffi_call(cap, oo_str_lit(sym_destroy), oo_str_lit("v"), oo_str_lit("p"), r_create.val);
  if (!r_dest.ok) { dlclose(h); return 1; }

  /* 6. dlclose */
  dlclose(h);

  remove(plugin_src);
  remove(plugin_so);
  printf("OK\tdlopen_ffi\tFull shared library round-trip (open/sym/call/close) verified\n");
  return 0;
}

int main(void) {
  long long cap = oo_cap_grant_ffi();
  int fails = 0;

  fails += test_repr_c_layout();
  fails += test_outparam_render_protocol(cap);
  fails += test_struct_by_value(cap);
  fails += test_dlopen_roundtrip(cap);

  if (fails == 0) {
    printf("PASS\tc_abi_layout\tAll C-ABI layout & FFI round-trip tests passed\n");
    return 0;
  }
  return 1;
}
