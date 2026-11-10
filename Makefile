OODA_COMPILER ?= /Projects/openOODA-core/oodac/bin/oodac
export OODA_COMPILER
OODAC_BIN ?= $(OODA_COMPILER)
export OODAC_BIN
OODA_READDIR ?= /Projects:/tmp:/usr:/lib:/lib64
OODA_WRITEDIR ?= $(CURDIR):/tmp
OO_LIST_AMBIENT_QUOTA ?= 8589934592
BIN := bin/openooda
TESTBIN := bin/test_functional
TESTBIN2 := bin/test_refusal
REPO_NAME := openooda
VER := 2.11.138
SRC := $(shell find . -name '*.oo' -not -path './.git/*' -not -path './bin/*' -not -path './dist/*' -not -path './.ooda-cache/*' | sort)

OODA_OODAR_ROOT ?= /Projects/openOODA-core/oodar/core
export OODA_OODAR_ROOT
ENV := OO_LIST_AMBIENT_QUOTA=$(OO_LIST_AMBIENT_QUOTA) OO_LINT_ROOTS=$(CURDIR) OODA_COMPILER=$(OODA_COMPILER) OODAC_BIN=$(OODAC_BIN) OODA_FS_READDIR=$(OODA_READDIR) OODA_FS_WRITEDIR=$(OODA_WRITEDIR) OODA_OODAR_ROOT=$(OODA_OODAR_ROOT) OODA_NO_JAIL=1

.PHONY: all build verify test check line-cap file-law academy density vocab shape link-law lint-oo-size clean

all: build verify test

build: $(BIN)

$(BIN): $(SRC)
	@mkdir -p bin .ooda-cache
	$(ENV) $(OODA_COMPILER) build cli/main.oo -o $(BIN)
	@chmod +x $(BIN)
	@echo "built $(BIN)"

line-cap:
	@violations=0; \
	for f in $$(find . -name "*.oo" -o -name "*.oot" | grep -v "/.git/" | grep -v "/bin/" | grep -v "/dist/" | grep -v "/.ooda-cache/"); do \
		n=$$(wc -l < "$$f"); \
		if [ $$n -gt 256 ]; then \
			echo "VIOLATION: $$f = $$n lines (exceeds 256)"; violations=$$((violations+1)); \
		fi; \
		code=$$(grep -vE '^[[:space:]]*(//.*)?$$' "$$f" | grep -cvE '^[[:space:]]*import[[:space:]]+"'); \
		if [ "$$code" = "0" ]; then continue; fi; \
		if [ $$n -lt 16 ]; then \
			echo "VIOLATION: $$f = $$n lines (under 16-line floor, not a shim)"; violations=$$((violations+1)); \
		fi; \
	done; \
	if [ $$violations -gt 0 ]; then echo "FAIL: $$violations files violate the Page Rule"; exit 1; fi; \
	echo "PASS: Page Rule sizing (16-256 lines, shims exempt from floor) holds"

file-law:
	@forbidden="py js ts rb pl json yaml toml"; \
	violations=0; \
	for ext in $$forbidden; do \
		found=$$(find . -name "*.$$ext" -not -path "./.git/*" -not -path "./bin/*" -not -path "./dist/*" -not -path "./.ooda-cache/*" 2>/dev/null | head -3); \
		if [ -n "$$found" ]; then \
			echo "VIOLATION: .$$ext forbidden:"; echo "$$found"; violations=$$((violations+1)); \
		fi; \
	done; \
	if [ $$violations -gt 0 ]; then echo "FAIL: file-law violations"; exit 1; fi; \
	echo "PASS: file law holds"

academy:
	@failures=0; \
	for f in $$(find . -name "*.oo" -not -path "./.git/*" -not -path "./bin/*" -not -path "./dist/*" -not -path "./.ooda-cache/*"); do \
		header=$$(head -7 "$$f"); \
		missing=""; \
		echo "$$header" | grep -q "^// # "        || missing="$$missing title"; \
		echo "$$header" | grep -q "^// Logline:"  || missing="$$missing logline"; \
		echo "$$header" | grep -q "^// Setup:"    || missing="$$missing setup"; \
		echo "$$header" | grep -q "^// Beats:"    || missing="$$missing beats"; \
		if [ -n "$$missing" ]; then \
			echo "FAIL: $$f missing Academy element(s):$$missing"; failures=$$((failures+1)); \
		fi; \
	done; \
	if [ $$failures -gt 0 ]; then echo "FAIL: $$failures academy header violations"; exit 1; fi; \
	echo "PASS: academy headers hold"

density:
	@violations=0; \
	for d in $$(find . -type d -not -path "./.git*" -not -path "./bin*" -not -path "./dist*" -not -path "./.ooda-cache*"); do \
		n=$$(ls "$$d"/*.oo "$$d"/*.oot 2>/dev/null | grep -v '\*' | wc -l); \
		if [ $$n -gt 8 ]; then \
			echo "VIOLATION: $$d holds $$n pages (exceeds 8)"; violations=$$((violations+1)); \
		fi; \
	done; \
	if [ $$violations -gt 0 ]; then echo "FAIL: $$violations directories exceed density bound"; exit 1; fi; \
	echo "PASS: directory density (<= 8 pages per directory) holds"

vocab:
	@if grep -riE "sovereign|Pillar [0-9]|moonshot|dogfight|bootstrap|Stage [0-9]" --include="*.oo" --include="*.oot" . ; then \
		echo "FAIL: banned vocabulary found"; exit 1; \
	fi; \
	echo "PASS: vocabulary check holds"

shape:
	@mkdir -p .ooda-cache; : > .ooda-cache/shape.now; \
	for f in $$(find . -name "*.oo" -not -path "./.git/*" -not -path "./dist/*" -not -path "./.ooda-cache/*" -not -path "./bin/*"); do \
		awk '/^[[:space:]]*(pub[[:space:]]+)?fn[[:space:]]/ { if (started) { len = NR - start; if (len > 64) print "FNLEN|$$f|" fn "|" len } started = 1; start = NR; if ($$1 == "pub") fn = $$3; else fn = $$2; gsub(/\(.*/, "", fn) } END { if (started) { len = NR - start + 1; if (len > 64) print "FNLEN|$$f|" fn "|" len } }' "$$f" >> .ooda-cache/shape.now; \
		n=$$(grep -cE "^[[:space:]]*(pub[[:space:]]+)?fn " "$$f" || true); \
		if [ "$$n" -gt 8 ]; then echo "SHAPE|$$f|-|$$n" >> .ooda-cache/shape.now; fi; \
	done; \
	violations=0; \
	while IFS='|' read -r kind path name value; do \
		[ -z "$$kind" ] && continue; \
		echo "VIOLATION: shape law $$kind|$$path|$$name|$$value"; violations=$$((violations+1)); \
	done < .ooda-cache/shape.now; \
	rm -f .ooda-cache/shape.now; \
	if [ $$violations -gt 0 ]; then echo "FAIL: $$violations shape violations"; exit 1; fi; \
	echo "PASS: shape law holds (<=8 fns/page, <=64 lines/fn)"

link-law:
	@violations=0; \
	for f in $$(find . -type l -not -path "./.git/*" 2>/dev/null); do \
		echo "VIOLATION: symbolic link $$f"; violations=$$((violations+1)); \
	done; \
	for f in $$(find . -type f -links +1 -not -path "./.git/*" 2>/dev/null); do \
		echo "VIOLATION: hard link $$f"; violations=$$((violations+1)); \
	done; \
	if grep -qE '(^|[^a-zA-Z_-])ln[ ]-s' Makefile; then \
		echo "VIOLATION: the Makefile creates a symbolic link"; violations=$$((violations+1)); \
	fi; \
	for f in $$(find bin dist -maxdepth 1 -type f 2>/dev/null); do \
		if [ ! -L "$$f" ] && [ "$$(stat -c '%h' "$$f")" != "1" ]; then \
			echo "VIOLATION: $$f is not a standalone binary"; violations=$$((violations+1)); \
		fi; \
	done; \
	if [ $$violations -gt 0 ]; then echo "FAIL: $$violations link law violations"; exit 1; fi; \
	echo "PASS: link law holds (no symbolic link, no hard link, standalone binaries)"

lint-oo-size:
	@violations=0; \
	pages() { find . \( -name '*.oo' -o -name '*.oot' \) -not -path './.git/*' -not -path './bin/*' -not -path './dist/*' -not -path './.ooda-cache/*'; }; \
	v=0; for f in $$(pages); do \
		n=$$(wc -l < "$$f"); \
		if [ $$n -gt 256 ]; then echo "VIOLATION: line law $$f = $$n lines"; v=$$((v+1)); fi; \
		code=$$(grep -vE '^[[:space:]]*(//.*)?$$' "$$f" | grep -cvE '^[[:space:]]*import[[:space:]]+"'); \
		if [ "$$code" != "0" ] && [ $$n -lt 16 ]; then echo "VIOLATION: line law $$f under 16-line floor"; v=$$((v+1)); fi; \
	done; \
	if [ $$v -gt 0 ]; then violations=$$((violations+v)); else echo "PASS: page lines (16..256, shims exempt)"; fi; \
	v=0; for f in $$(pages); do \
		nf=$$(grep -cE '^[[:space:]]*(pub[[:space:]]+)?fn ' "$$f" || true); \
		if [ "$$nf" -gt 8 ]; then echo "VIOLATION: fn count $$f = $$nf (exceeds 8)"; v=$$((v+1)); fi; \
		awk '/^[[:space:]]*(pub[[:space:]]+)?fn[[:space:]]/ { if (started && NR - start > 64) { printf "VIOLATION: fn length %s %d lines\n", FILENAME, NR - start; bad = 1 } started = 1; start = NR } END { if (started && NR - start + 1 > 64) { printf "VIOLATION: fn length %s %d lines\n", FILENAME, NR - start + 1; bad = 1 } exit bad ? 1 : 0 }' "$$f" || v=$$((v+1)); \
	done; \
	if [ $$v -gt 0 ]; then violations=$$((violations+v)); else echo "PASS: function law (<= 8 fns/page, <= 64 lines/fn)"; fi; \
	v=0; for d in $$(pages | xargs -n1 dirname | sort -u); do \
		n=$$(ls "$$d"/*.oo "$$d"/*.oot 2>/dev/null | grep -v '\*' | wc -l); \
		if [ $$n -gt 8 ]; then echo "VIOLATION: density $$d = $$n pages"; v=$$((v+1)); fi; \
	done; \
	if [ $$v -gt 0 ]; then violations=$$((violations+v)); else echo "PASS: directory density (<= 8 pages per directory)"; fi; \
	if [ $$violations -gt 0 ]; then echo "FAIL: $$violations lint-oo-size violations"; exit 1; fi; \
	echo "PASS: lint-oo-size holds the Page Rule over the tree"

check:
	@for f in $$(find . -name "*.oo" -not -path "./.git/*" -not -path "./bin/*" -not -path "./dist/*" -not -path "./.ooda-cache/*"); do \
		$(ENV) $(OODA_COMPILER) check "$$f" > /dev/null || exit 1; \
	done; \
	echo "PASS: oodac check holds on all .oo files"

verify: line-cap file-law academy density vocab shape link-law lint-oo-size check

test: $(BIN)
	@mkdir -p .ooda-cache
	@$(ENV) $(OODA_COMPILER) build tests/test_functional.oo -o $(TESTBIN) > /dev/null
	@$(ENV) $(OODA_COMPILER) build tests/test_refusal.oo -o $(TESTBIN2) > /dev/null
	@PATH=/nonexistent $(ENV) ./$(TESTBIN) | grep -q "PASS: functional" && echo "PASS: functional suite under PATH=/nonexistent"
	@PATH=/nonexistent $(ENV) ./$(TESTBIN2) | grep -q "PASS: refusal" && echo "PASS: refusal suite under PATH=/nonexistent"
	@PATH=/nonexistent $(ENV) ./$(BIN) check . | grep -q "verify OK" && echo "PASS: openooda check ."
	@PATH=/nonexistent $(ENV) ./$(BIN) check | grep -q "verify OK" && echo "PASS: openooda check"
	@PATH=/nonexistent $(ENV) ./$(BIN) verify | grep -q "verify OK" && echo "PASS: openooda verify"
	@PATH=/nonexistent $(ENV) ./$(BIN) audit | grep -q "verify OK" && echo "PASS: openooda audit"
	@PATH=/nonexistent $(ENV) ./$(BIN) status | grep -q "PASS" && echo "PASS: openooda status"
	@PATH=/nonexistent $(ENV) ./$(BIN) cards | grep -q "defense.md" && echo "PASS: openooda cards"
	@rc=0; PATH=/nonexistent $(ENV) ./$(BIN) --unknown-flag-zzz > /dev/null 2>&1 || rc=$$?; [ "$$rc" = "2" ] && echo "PASS: --unknown-flag-zzz refusal exits 2"
	@rc=0; PATH=/nonexistent $(ENV) ./$(BIN) --persona oocoder > /dev/null 2>&1 || rc=$$?; [ "$$rc" = "2" ] && echo "PASS: --persona refusal exits 2"
	@rc=0; PATH=/nonexistent $(ENV) ./$(BIN) check ../openOODA > /dev/null 2>&1 || rc=$$?; [ "$$rc" = "2" ] && echo "PASS: traversal operand refusal exits 2"
	@rc=0; PATH=/nonexistent $(ENV) ./$(BIN) check /etc > /dev/null 2>&1 || rc=$$?; [ "$$rc" = "2" ] && echo "PASS: non-root target refusal exits 2"
	@PATH=/nonexistent $(ENV) ./$(BIN) --help | grep -q "$(REPO_NAME) $(VER)" && echo "PASS: --help"
	@PATH=/nonexistent $(ENV) ./$(BIN) --version | grep -q "$(VER)" && echo "PASS: --version"
	@PATH=/nonexistent $(ENV) ./$(BIN) --self-test | grep -q "PASS" && echo "PASS: --self-test"
	@PATH=/nonexistent $(ENV) ./$(BIN) about | grep -q "Binary       :" && echo "PASS: about"
	@PATH=/nonexistent $(ENV) ./$(BIN) about | grep -q "Organization : openOODA" && echo "PASS: about org"
	@PATH=/nonexistent $(ENV) ./$(BIN) theme ooda-dark | grep -q "openooda" && echo "PASS: theme ooda-dark"
	@PATH=/nonexistent $(ENV) ./$(BIN) check --json | grep -q '"pass":true' && echo "PASS: check --json"
	@PATH=/nonexistent $(ENV) ./$(BIN) --json | grep -q '"component":"openooda"' && echo "PASS: bare --json verdict envelope"
	@echo "ALL TESTS PASSED"

clean:
	@rm -rf bin dist .ooda-cache
