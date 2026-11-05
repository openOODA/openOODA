# Naming & Single-Responsibility Audit — Reconciled Consensus

**Reconciler:** Devin `wR:p2` (swe-2-max) — third pass, independent verification
**Date:** 2026-11-05
**Inputs:**
- `naming-audit-mcode.md` (mcode / MiniMax-M3.1-Flash, `w3:p1` — 788 lines; token-collision matrix method) — cited as **M§n**
- `naming-audit-devin.md` (Devin `wR:p1` — 283 lines; physical-subtree + RFC-conformance method) — cited as **D§n**

**Method:** Both audits were independent and read-only (no compiler, build, test, or binary executed). This third pass re-verified **every contested, load-bearing, or divergent claim directly against the tree** — persona dispatch sources, Makefiles, `catalog/index`, RFC 0012 §2.3 (`rfcs/0012:139-145`), `northstar.oot`, and directory inventories. Claims that failed verification are listed in §5 **[ERRATA]**. A prior draft of this file written by `wR:p1` was superseded by this one after its `oohealthd` RFC misread and two inherited errata were caught (§5).

**Conventions:** repo paths abbreviated to `org/name` (e.g. `apps/ooflash` = `openOODA-apps/ooflash`).

---

## 0. Bottom line

Two independent auditors, different models, different extraction methods, converged on one root cause:

> **The fleet does not have a bad-names problem — it has a name-ownership problem.** Repo dirs ↔ `BIN` names are nearly perfectly consistent; the defects are persona/repo tokens with **two owners or none**, absorptions declared but never enacted, canonical names existing only on paper, and at least four pairs of repos claiming *each other*.

The single most consequential verified fact: **21 signed, publicly installable `catalog/index` package names are simultaneously persona tokens of other binaries** — the install surface and the runtime surface disagree about who owns a name.

- **16 of 20** top findings are shared or mutually reinforcing (§1–2)
- **11** verdict-level divergences adjudicated against the tree + RFC (§4)
- Each auditor caught serious defects the other missed entirely (§3) — the audits are complementary, not redundant
- Action plan: **5 ownership decisions → ~23 zero-risk archives → 21 catalog withdrawals → ~14 renames → 6 splits → substrate dedup → registry/gates** (§7)

---

## 1. Executive agreement — verified joint findings

| # | Joint finding | Devin | mcode | Verified here |
|---|---------------|:-----:|:-----:|:-------------:|
| C1 | **Duplicate persona embeddings** (same token, 2+ hosts, forked subtrees) | F2, §4.1 (7 tokens) | §4.1–4.4 (57 dual-host, 82-token union — **superset**) | ✅ dispatch sources |
| C2 | **Catalog-published collisions** — signed packages that are also personas | §4.3 families | F2/§4.2/§5.4 | ✅ all **21** in `catalog/index` |
| C3 | **`oobuild-fleet`↔`oodeploy` mutual absorption cycle** | F1, §4.2 | §3.11 | ✅ both Makefiles |
| C4 | **RFC inversions** — code absorbs A→B where RFC declares A canonical | F1, §4.2 (4 pairs) | §5.3 partial | ✅ RFC L5/L7 lists |
| C5 | **RFC-canonical ghost names** | F3, §2.2 (9) | §6.1 | ✅ RFC §2.3 |
| C6 | **Substrate/template cloning** — repo count overstates product count ~10–20× | F5, §3.1 | F7, §3.3, §3.7 | ✅ name-token diffs |
| C7 | **Absorbed repos still ship standalone binaries** — absorption declared, never enacted | §4.1/§5.1 | F8, §5.1 | ✅ `bin/` artifacts |
| C8 | **`sys_argv0` contract survives Rule 1.25** (source + docs) | F7, §5.5.7 | F4/§4.7, F11 | ✅ `ooimage/main.oo:62`, `llms.txt:35`, `oooda-engine/AGENTS.md` §4.1 |
| C9 | **`oomedia`→`ooflash` split = correct remediation** | §3.2 | §3.1 (pre/post states) | ✅ post-split tree |
| C10 | **`ooflash` adds host-binary execs** (`dd`,`sha256sum`,`sync`,`truncate`) — Rule-1.25 regression on 2026-11-05 | §4.4 | F9, §3.1 | ✅ `rawio.oo` execs |
| C11 | **`oote` misnamed** — theming engine squatting a reserved axis | F4 (tee namespace) | §2.15 (`ootext` axis) | ✅ both true |
| C12 | **`oosession`+`policy/` is the RFC's `ooauthd`** | §2.2, §5.3 | §6.1 ghost | ✅ `oosession/policy/` = 8 pages |
| C13 | **`oofalse` in RFC agents list = typo for `oofalsify`** (and collides with `tools/oofalse`) | §5.5.1 | §6.1 | ✅ RFC `:145` |
| C14 | **Tools exec-relay to C binaries** — 8 persona tables shell out to GNU/OpenSSL/GPG | §4.4 partial | §3.10 (deepest) | ✅ 8 `personas.oot` files |
| C15 | **0 symlinks / 0 hardlinks fleet-wide** — Rule 1.25 physically holds | §1, §7 | §8 | ✅ |
| C16 | **Catalog index ↔ disk: zero drift** — but only L3 is registered | §2/§6 | §7.11 | ✅ 260 names / 256 pkgs |

---

## 2. The duplicate-embedding set — both audits, fully verified

| Token | Host A | Host B | Consensus owner |
|-------|--------|--------|-----------------|
| `oodns-cloud` | `oomesh` | `oogateway` (3rd: own repo) | **`oomesh`** (RFC L6 mesh pairing); strip from `oogateway` |
| `ooqueue` | `oodb-dist` | `oosched-cloud` | **`oodb-dist`** (queue = data plane; `oosched-cloud` is non-canonical anyway) |
| `ooclip` | `oofiles` | `ooportal` | **`ooportal`** (capability-grant boundary is the honest owner) |
| `ooshot` | `oofiles` | `ooportal` | **`ooportal`** (same) |
| `ootaskmgr` | `oofiles` | `oocockpit` (itself a `oopanel` persona) | **`oopanel`** transitively — a persona cannot host a persona |
| `ooarchitect` | `oogovern` (30-pg subtree, byte-identical to standalone) | `oooda-engine` (`persona/architect.oo` — rewritten variant that **drops `ooarch_basename`**) | **`oogovern`** — its copy preserves SSoT; retire engine's divergent variant |
| `oohealthd` | `ooinit` (`healthd/` subtree, 8 pages) | standalone repo ships `bin/oohealthd` | **`oohealthd` repo** — it is in RFC's L2 canonical-8; strip `ooinit/healthd/` (see §4.4) |
| `engine` (alias) | `oooda-engine` (`meta.oo:24`) | `ooherdr` (`meta.oo:34`) | one side drops it — recommend `ooherdr` keeps, `ooooda` loses on rename |
| `sha256sum` (token) | `oohash` relay | `oob3sum` relay **+ `ooflash/digest.oo`** | digest host (§4.7); `ooflash` must go native anyway |

---

## 3. Unique findings (one auditor only)

### 3.1 mcode-only — spot-verified in this pass

| Finding | Evidence | Consensus adoption |
|---|---|---|
| **`std/hw` kernel stack** — 112 impl `.oo` pages across 9 subdirs in a "standard library"; 2 verbatim-identical cap-space pages vs `ookernel-ob`; `std/anchor.oo` vs `std/hw/anchor.oo` self-contradict | M§2.1/§3.2. Verified: exactly 112 in subdirs (127 incl. top-level theory pages) | **SPLIT `std`→`std`+`std-hw`.** The largest single-scope violation in the fleet; devin missed it entirely (called L0 "cleanest org") |
| **`oohash`↔`oob3sum` mutual persona cycle** | `oohash/ipc/dispatch_persona.oo:33` ↔ `oob3sum/ipc/persona_dispatch.oo:32` — verbatim | Critical — feeds §4.7 |
| **`ooimage` overclaim + port bug** — README:76 promises L1 ISO + L2 UEFI/Firecracker; only container-string gen exists; `ooda_inference.oo:24,28`=`11434` vs `:39`=`11435` | M§2.2/F6. Verified | RENAME `oocontainer`; fix port bug (a live functional defect) |
| **`oovm-ui` overclaim** — README promises KVM VM manager; sole domain page is a 42-line `/proc/meminfo`+`loadavg` reader | M§2.7. Verified (zero qemu/kvm in domain code) | RENAME `oohostmon` |
| **Hidden aliases**: `oocompctl`→`oocomp`, `oowallpaper`→`oowall`, `oonotify`→`ootoast`, `ooidle`/`ooscreensaver` self-absorbed by `oolock` | M§4.6 | Add to ownership table |
| **`oodeepseek` vendor persona** inside `oocoder` + hardcoded `:11435` | M§2.13. Verified | RENAME `oocoder-deepseek` |
| **`oodrv-net` overclaim** — promises e1000e/RTL8125; delivers a 7-word frame codec; own union persona already `oodrv-io` | M§2.10 | RENAME `oodrv-io` |
| **`ookernel-hal-x86` overclaim** — x86-named host covering 3 archs | M§2.11 | RENAME `oohal` |
| **`oooda-engine` stutter** | M§2.12 | RENAME `ooooda` |
| **`bedaisy_gate` in `ookernel-mm`** — BattlEye/Destiny-2 anti-cheat IOMMU gate inside a memory manager; duplicated `ookernel-ob/nt/` | M§3.4. Verified header | Extract → `ookernel-ob/nt/` before archive |
| **`oorouter` L6 files** (`core/fleet.oo`,`gpu_schedule.oo`) duplicating `ooinfer-grid` | M§3.5. Verified | Delete both files; fold remainder → `ooherdr` |
| **`ooherdr` 4-domain split** — roster + cluster failover + `oomux` TUI + hardcoded vendor-driver registry | M§3.6. Verified | Extract `oomux` + registry |
| **`lsp`/`mcp` ship-name debt** — `dist/mcp` vs `ooda-mcp`; 5-step legacy fallback `tui/mcp_client.oo:79`; `install.sh` puts bare `lsp`/`mcp` in `~/.openooda/bin` | M§2.8/§7.9/§7.10. Verified | Uniform `ooda-lsp`/`ooda-mcp`; retire bare names from install surface |
| **`oodar` metadata contradictions** (lib name / layer / file-count) | M§2.9 | Doc fix |
| **`oollama` anomaly** — only tools repo correctly absent from catalog; absorbed into `ooaid` | M§5.5. Verified | Archive repo; keep persona |
| **Phantom `unix_consolidation_blueprint.md`** — directive cites a nonexistent doc | M§6.4. Verified absent | Fix directive → cite RFC 0012 |
| **README/AGENTS drift fleet-wide** — kernel page claims 10–16 vs actual 30–37; `95/95` vs `80` assertions; 11 agents repos one version behind; DE org profile says 20 lists 18, byte-identical stub ×20 | M§7.3/§7.4 | Doc sweep checklist |
| **`oodac` 4 binary copies; kernel `SRC` omits `fs/fsprobe.oo` ×6; "ELF64 boot image" README lie ×6; `oodac_cluster.sh` fallback; `install.sh` 8-component surface** | M§7.5–7.10 | Hygiene + build-correctness |
| **Hardcoded fleet hostnames/Tailscale IPs** — `status.oo:176-178` hard bindings; `fanout.oo:91`,`quota_ledger.oo:76-77` env-defaults; `ooaid` embeds hostnames in *identifiers* | M§7.8 (F12). Verified | Hard bindings must go; defaults documented; redaction table = declared exemption |
| **Conformance sweep** — 246 core files >8 fns (worst `ai_multimodal.oo`=87); 1,857 fns >40 lines; duplicated 200-line `poly1305_mac` | M§8 | Declare shim exemption class + schedule cleanup; `boundary_257_lines.oo` needs allowlist entry |
| **Negative-tested pairs** — `ooconsent`≠`ooconsensus`, `oostore`≠`oostore-cas`, `oobilling`/`ooquota`/`ootelemetry` distinct | M§2.18 | Good discipline; no action |

### 3.2 devin-only — spot-verified in this pass

| Finding | Evidence | Consensus adoption |
|---|---|---|
| **`oosqllite` committed typo** — dir/`BIN`/AGENTS/catalog all spell "sqllite"; 0-byte README | D F4. Verified (catalog:197) | RENAME `oosqlite` (or fold `ooquery`) |
| **104 skeleton stubs** — uniform 13-file `cli+read+core/{cap,codec,engine,ring,table}` skeleton; READMEs uniformly claim "Native X TOOL" (`ooip show <file>` greps a file) | D F8. Sampled `ooip`/`oobiew`/`oonaa` | Reclassify: **unimplemented backlog, NOT "absorbed"** — changes archive verdict for ~104 repos |
| **6 stale `oofzf` AGENTS.md copies** (`ooclock,oocurl,oops,oosed,otar→ootar,ootree`; `oocurl` says "operating on `oofzf`") | D F9. All 6 verified | Regenerate per-repo |
| **Workspace debris** — `/Projects/openOODA/8` (74B), `bracket_probe{,2}.txt`, ~375 `.ooda-cache/` dirs | D F10. Verified | Hygiene sweep |
| **Cryptic/hazard names** — `oonaa`, `ooripl`, `oobiew` (vs `DE/ooview`), `oobound`/`ooboundary`, `oocsplt` (truncated csplit), `ooss`/`oossh`/`oossl` trio, `oood` (vs `oooda` prefix), `oorev` (rev vs revocation), `oomenubar` (DE chrome in L3) | D§2.1. All repos verified exist | Rename/merge candidates in Phase 5 |
| **Duplicate-domain pairs** — `oomeminfo`/`oofree`, `oofilter`/`ooawk`, `ootls`/`oossl` (both declare upstream `openssl`), 4 watchers, 3 progress bars | D§2.1/§4.3 | Merge each to one owner |
| **Ghost names** — `oozip` (only `oounzip` exists — unzip with no zip producer), `oocage` (`ooaid` README ref), `ooide`, `oomsg` | D§2.2. Verified absent | Create or scrub references |
| **`oocockpit` nests canonical `ooagent-hud`** — shell-inside-a-shell carrying an RFC product | D§3.2/§4.2. Verified | Extract `ooagent-hud` **before** `oocockpit`→`oopanel` demotion |
| **Missing-coverage gaps** — `oodate` (verified absent), `oodd`, `ooecho`, `oocal`, `ooed`, `ootee`, `oozip` | D§4.4 | `ooflash` wraps host `dd` partly because **no `oodd` exists** — fill or persona-map |
| **Missing `link-law` Makefile gate** in all cloud + agents repos | D F7 | Phase-8 tooling |
| **`openOODA-tools.github.io`** docs-site repo inside tools org — inflates count 257→258, breaks `oo*` namespace | D§2.1. Verified present | Declare non-product in `northstar` |
| **`oollama` layer mislabel** ("Layer 4" claim on an L3 repo absorbed into L2) | D§2.3 | Doc fix; complements mcode's anomaly finding |
| **Absorption into non-canonical hosts** — `oopolicyd`→`oosession` (non-RFC), `oopowerd`→`oodevd` (non-RFC) | derived: D§5.1 + RFC check | Staging waste — `oosession`→`ooauthd` rename rescues one; retarget `oodevd`'s `power/` subtree to `oosysbus` or `oohealthd` |
| **`oostructureddiff` family collapse** — 5 differ repos → one host, format personas | D§5.4 | Adopted |
| **`oocat` triple mandate** (cat+less+highlight), `ooclock` triple (clock+stopwatch+pomodoro), `ooenv` triple | D§3.2 | Narrow or accept as documented scope |

---

## 4. Divergences — adjudicated

| # | Dispute | Devin | mcode | Evidence | **Consensus ruling** |
|---|---------|-------|-------|----------|----------------------|
| 4.1 | DE shell-host naming | Keep `oofiles`/`oopanel` names | RENAME → `ooshell`/`oogrant`; §6.1 wrongly lists `ooshell` as RFC ghost | `ooshell` appears in **no** governing doc — verified fleet-wide | **Keep `oopanel`/`oofiles`/`ooportal` names.** `ooshell` is mcode's invented proposal (marked [ERRATA] as an "RFC ghost"); `ooportal` matches the freedesktop pattern, `ooshell` would collide conceptually with tools `oosh`. Scope fix, not rename. |
| 4.2 | `oomail`/`oochat` | Prefer `oomail` host (RFC; superset domain) | Lists `oomail`→`oochat` archive uncontested | RFC `:143` L5: `oomail` canonical, `oochat` absent; `oochat/personas/oomail/` (4 impl pages) > standalone `oomail` | **DECISION REQUIRED.** Two coherent rulings: (a) RFC-faithful — `oomail` canonical comms host, `oochat`→persona; (b) pragmatic — keep `oochat` host (larger impl, already embedded) + amend RFC to swap. Either way the loser is archived and the winner keeps the bigger impl. Neither audit may pick unilaterally. |
| 4.3 | `ooarchitect` host | flagged dup, no pick | arbitration needed; noted divergent impls | `oogovern/ooarchitect/` byte-identical to standalone; `oooda-engine`'s variant drops `ooarch_basename` | **`oogovern`** — byte-identical copy preserves single-source-of-truth; retire `oooda-engine`'s divergent variant. |
| 4.4 | `oohealthd`/`ooinit` | fold OR keep canonical | SPLIT `healthd/` out of `ooinit` | **RFC `:140` L2 list explicitly includes `oohealthd`**; `ooinit/healthd/`=8 pages; standalone repo ships `bin/oohealthd` | **`oohealthd` stays canonical per RFC — strip `ooinit/healthd/` embed.** (A prior consensus draft claimed "RFC L2 has no oohealthd" — [ERRATA], the name is literally in the list.) mcode's split verdict lands at the same endpoint: one owner, the canonical repo. Keep `oosvc-mgr` inside `ooinit`. |
| 4.5 | `oocoder`/`ooreviewer` | un-invert per RFC (`oocoder` canonical) | demote `oocoder` into `ooreviewer` — but §5.6 KEEP table lists **both**, internally inconsistent | RFC `:145` L7 has `oocoder`, no `ooreviewer`; `ooreviewer/oocoder/` = 30 pages | **`oocoder` canonical; `ooreviewer` demoted to persona** (review is a coding-agent mode). Strip the inverted `ooreviewer/oocoder/` subtree. If owner wants both as products, RFC needs a 9th slot — owner decision. |
| 4.6 | `-cloud` suffix | noted collision | RENAME `oodns-cloud`/`oosched-cloud`/`ooregistry-cloud` → drop suffix | `tools/oodns` exists → `oodns-cloud`→`oodns` would *create* a stem collision | **Do not rename.** The suffix is load-bearing disambiguation on the install PATH. Resolution = absorption into `oomesh`/`oodeploy`/`oostore`, which makes the repo names moot anyway. |
| 4.7 | `oob3sum` vs `oohash` | digest overlap noted, no owner pick | spec ambiguous — RFC→`oob3sum`, directive→`oohash` | mutual persona cycle verified; directive lists `oohash`, RFC §2.2.4 lists `oob3sum` | **Recommend `oohash` as the single digest host** — on naming grounds (this audit's own criterion): the host serves sha256/sha512/md5/cksum/b3sum personas; naming a multi-algorithm host after one algorithm (`oob3sum`) is the same overclaim defect flagged elsewhere. Break the mutual cycle, archive `oob3sum`→persona, **amend RFC** (or keep `oob3sum` + amend directive — owner picks; one owner mandatory). `oosha256`/`oosha512`/`oomd5`/`oocksum`→personas. |
| 4.8 | `core` names clean? | "cleanest org; names honest" | `lsp`/`mcp`/`cli`/`tui`/`opm` = generic global names + artifact-name mismatch | `mcp/Makefile:26`→`dist/mcp` vs CI `ooda-mcp`; `install.sh:105` bare names | **Names are honest (D) but non-namespaced (M).** Ship artifacts uniformly as `ooda-lsp`/`ooda-mcp` (already CI names); retire bare `lsp`/`mcp`/`cli`/`tui`/`opm` from `~/.openooda/bin`. Repo renames `oocli`/`ootui`/`oopm` = optional, lower priority. |
| 4.9 | `oosession`→`ooauthd` | proposed rename | ghost noted, no rename target | `oosession/policy/`=8 pages; RFC keeps `ooauthd` | **Rename `oosession`→`ooauthd`** (session+policy IS the auth daemon) — closes the ghost + names the domain correctly. |
| 4.10 | Nested personas (host is itself a persona) | `oocockpit` nesting noted | `oocockpit`,`oolock` "host is also a persona" → demote | dispatch tables verified | **Flatten: a canonical host must not itself be a persona of another host.** `oocockpit`,`oolock`,`ooreviewer`→persona-only; `ooagent-hud` subtree → `oopanel` (or re-canonicalized per RFC). |
| 4.11 | `oobazaar` | 4 backends = overlap | SPLIT per backend | `oobazaar/README.md:5-9` verified 4 install backends | **Keep one store; thin backend adapters** (bazaar=store is an honest name; 4 provisioning backends behind adapters is defensible). Split only if adapters prove fake. |

---

## 5. Errata — claims that failed verification

### In the two audits

| Auditor | Claim | Reality | Disposition |
|---|---|---|---|
| mcode | "All **17** `openOODA-kernel` repos" (F7/§3.3) | **16** (`ls` + `llms.txt` agree) | Cosmetic; finding stands |
| mcode | "**20** catalog-exposed collisions" (F2/§4.2/§5.4 text) | mcode's own table lists **21** rows; all 21 verified in `catalog/index` | Correct count = **21** |
| mcode | `ooshell` = "RFC target name that does not exist" (§6.1) | `ooshell` appears in **no** `.oot`, `.md`, or `.oo` file except mcode's own audit | Reclassified: optional proposal (§4.1), not a spec ghost |
| devin | `oowm`/`ooterm` "**file-for-file identical** trees" (F5/§3.1) | Identical file *names* + tree shape (28 files); contents differ — name-token clones | Overstated; structural-clone point stands |
| devin | "**378** product subdirectories" | ~379–382 depending on `status`/`8`/`github.io`/`ooflash` counting; RFC baseline 377 | Cosmetic |
| — | tools repo count | mcode 257 = `oo*` product dirs; devin 258 = + `github.io` | Reconciled: **257 product + 1 docs-site** |
| devin | "104 skeleton stubs" | sampled-verified, not exhaustively counted | Treat as ±104 |

### In wR:p1's superseded consensus draft (recorded for transparency)

| Draft claim | Reality |
|---|---|
| §4.4: "RFC L2 canonical-8 has no `oohealthd`" | **False** — `rfcs/0012:140` lists `oohealthd` explicitly. Reversed the ruling (§4.4 above). |
| §2.3: `ooshell` listed among RFC ghosts | Inherited mcode's erratum; `ooshell` is no doc's target |
| "20 catalog-exposed" throughout | Inherited mcode's count; actual = **21** |

No verified claim in either audit was *fabricated* — error rate is low and cosmetic. Confidence in both source documents is high.

---

## 6. Reconciled master disposition table

### 6.1 READY TO ARCHIVE — single owner, subtree/impl verified, no RFC contradiction

*Read-only evidence; RFC 0011 parity/double-run gates remain unverified per repo.*

| Set | Repos → host |
|---|---|
| **apps (4 clean)** | `oosheet`→`oooffice(oodocs)`, `oodeck`→`oooffice`, `oopaint`→`oocanvas`, `oogit-ui`→`oostudio` |
| **apps (3 conditional)** | `oonotes`→`oooffice`, `oopdf`→`oooffice`, `oomail`→`oochat` — **blocked pending §4.2/RFC amendment** (RFC lists all three canonical) |
| **DE (7)** | `oowm`→`oocomp`, `oowall`→`oocomp`, `ooview`→`oofiles`, `ooedit`→`oofiles`, `oolaunch`/`ooshelf`/`ootoast`→`oopanel` |
| **OS (4 clean)** | `oodnsd`→`oonetd`, `oosvc-mgr`→`ooinit`, `oofs-ext4`→`oovfs`, `oofs-tmp`→`oovfs` |
| **OS (2 retarget)** | `oopolicyd`→`oosession`(→`ooauthd` rename rescues it), `oopowerd`→`oodevd` (**non-canonical host** — retarget subtree to `oosysbus`/`oohealthd` first) |
| **agents (5)** | `ooplanner`→`ooooda`, `ooeval`/`ooevolve`→`ooconsensus`, `ooredteam`→`oofalsify`, `oorelease`→`oogovern` |
| **tools (1)** | `oollama`→`ooaid` (the only correct catalog absence) |
| **core (1)** | `ooda`→`cli` (already a persona, `resolve.oo:59`) |

**Total mechanically ready ≈ 23** (mcode's 20 minus {`oonotes`,`oopdf`,`oomail`,`ooagent-hud`} + OS-6 + core-`ooda`).

### 6.2 CONDITIONAL — arbitration before archival

`ooclip`/`ooshot`→`ooportal` · `ootaskmgr`→`oopanel` · `oocockpit`,`oolock`,`ooreviewer`→demote (§4.10) · `ooarchitect`→`oogovern` (§4.3) · `oohealthd`→keep canonical (§4.4) · `oocoder`→canonical (§4.5) · kernel 12→rename-then-absorb per RFC (`oodrv-usb-hid`,`ookernel-iommu`,`ookernel-unikernel`,`oodrv-pci`,`oodrv-virtio`,`oodrv-display-gop`,`ookernel-mm`,`ookernel-ipc`,`ookernel-ob`,`ookernel-hal-arm64`,`ookernel-hal-riscv`,`ookernel-sched`) · cloud: `oodns-cloud`→`oomesh`-only, `ooqueue`→`oodb-dist`-only, `oobuild-fleet`→archive into `oodeploy` (cycle broken), `oocdn`→`oogateway`, `ooconsent`→`ooidentity`, `oorelay`→`oomesh`, `ooregistry-cloud`/`oostore-cas`→`oostore`, `ooinfer-grid`/`oosched-cloud`→`oodeploy` · catalog-21 → per §6.4.

### 6.3 CANONICAL — KEEP (honest names; may still need scope fixes)

- **core:** `oodac`,`oodar`,`cli`,`opm`,`tui`,`mcp`→`ooda-mcp`,`lsp`→`ooda-lsp`,`std` (+`std-hw` split)
- **kernel (RFC names):** `ookernel`,`ooboot`,`oohal`,`oodrv-storage`,`oodrv-io`,`oodrv-virt` — mapping decision needed for `oodrv-pci` (RFC's 6 don't obviously contain it)
- **OS:** `ooinit`,`oovfs`,`oonetd`,`oosysbus`,`ooaid`,`ooauthd`(=`oosession`),`oocontainer`(=`ooimage`),`oohealthd` + `oologd`/`ooaudiod` need homes (`oosysbus`/`oohealthd`)
- **tools:** RFC-64 shape; model consolidator `oocurl`; single-owner hosts `oohash`,`oocodec`(=`oobase64`),`ooarchive`,`oodiff`,`oosh`,`ootext`(create),`ootheme`(=`oote`),`oocat`,`ools`,`oojq`,`oogrep`,`oofind`,`oosort`,`oosed`,`ooawk`,`ootop`/`oowatch`(pick one),`oossl`
- **DE:** `oocomp`,`oopanel`,`ooportal`,`oofiles`,`ooterm`,`oosettings`,`oobazaar`,`oolock`(demote),`ooagent-hud`
- **apps:** `oobrowser`,`oostudio`,`oooffice`(=`oodocs`),`oocanvas`,`oomedia`,`oodaw`,`oopass`,`oohostmon`(=`oovm-ui`),`ooflash` + `oochat`/`oomail` winner
- **cloud:** `oomesh`,`oostore`,`oodeploy`,`oogateway`,`ooidentity`,`oodb-dist`,`ootelemetry`,`oobilling` (8 = RFC exactly)
- **agents:** `ooooda`(=`oooda-engine`),`ooherdr`(minus `oomux`+driver-registry),`ooquota`,`oofalsify`,`ooconsensus`,`oocoder`,`oomemory`,`oogovern` (+fold `oorouter`→`ooherdr`)

### 6.4 CATALOG — withdraw-or-dedupe (highest user impact)

**21** signed `catalog/index` packages that are also personas: archive repo + withdraw entry (recommended: `oosha256`,`oosha512`,`oomd5`,`oobase32`,`oobase58`,`oohex`,`oowget`,`oowget2`,`oofetch`,`oogzip`,`ooxz`,`oozstd`,`oounzip`,`oossl`,`oomcp`,`oomcprun`,`ooripl`,`oonotify`,`oobar`) — or withdraw the persona from the host. `oohash` survives per §4.7; `oob3sum`→persona + withdraw. **Precondition:** native persona implementation (the §3.10 exec-relay debt) — several can't ship until Phase 6 lands.

### 6.5 RENAME — agreed set

`oodocs`→`oooffice` · `ooimage`→`oocontainer` · `oovm-ui`→`oohostmon` · `oosession`→`ooauthd` · `ookernel-hal-x86`→`oohal` · `ookernel-boot`→`ooboot` · `ookernel-sched`→`ookernel` · `oodrv-net`→`oodrv-io` · `oodrv-nvme`→`oodrv-storage` · `oodrv-virtio`→`oodrv-virt` · `oooda-engine`→`ooooda` (+kill `engine` alias) · `oote`→`ootheme` (create `ootext`; `tee`→persona of `oocat`) · `oobase64`→`oocodec` · `oosqllite`→`oosqlite` · `oodeepseek`→`oocoder-deepseek` · artifacts `mcp`/`lsp`→`ooda-mcp`/`ooda-lsp` uniformly · `oobiew`/`ooboundary`/`oocsplt`/`oomenubar`/`oonaa` → per name-zoo dispositions.

### 6.6 SPLIT / SCOPE-FIX — agreed set

`std`→`std`+`std-hw` · `ookernel-mm`: extract `bedaisy_gate`→`ookernel-ob/nt/` · `oorouter`: delete L6-dup files, fold→`ooherdr` · `ooherdr`: extract `oomux`+driver-registry · `oofiles`: move `ooclip`/`ooshot`→`ooportal`, `ootaskmgr`→`oopanel`; keep `ooview`/`ooedit` · `oocockpit`: disassemble; `ooagent-hud` subtree→`oopanel` · `oobuild-fleet`: strip `oodeploy/`+`etc/oodeploy.conf` · `oorealm`: split `ooflathub`/`oowinrealm`/container; dedupe tier list vs `ooimage` (SSoT defect — both assert the canonical 3-container set) · `oobazaar`: narrow to adapters · `ooflash`: **native `.oo` for `dd`/`sha256sum`/`sync`/`truncate`** · `oofilter`→`ooawk`, `ootls`→`oossl`, `oomeminfo`→`oofree` merges · differ-zoo→`oostructureddiff` host.

---

## 7. Unified remediation sequence

Ordering principle (both auditors agree): **ownership before archival before rename** — renaming while a token has two owners multiplies ambiguity; archiving before ownership settles orphans personas.

1. **Publish the machine-readable persona-ownership table** — one row per token, exactly one winner (M§4.5/§9.1; D F2). `personas=` exists in `ooda.pkg` for only 3 repos fleet-wide; nothing else is safely decidable without it.
2. **Break the cycles** — `oohash`↔`oob3sum` (→`oohash` per §4.7 + RFC amendment) and `oobuild-fleet`↔`oodeploy` (→`oodeploy` per RFC).
3. **Arbitrate multi-host tokens** — `oodns-cloud`/`dns`→`oomesh`; `ooqueue`/`queue`→`oodb-dist`; §4.2/§4.5 owner decisions.
4. **Withdraw the 21 catalog-exposed double-ships** (§6.4) — fixes the *public* surface first.
5. **Archive the ~23 mechanically-ready repos** (§6.1) — after parity proof per repo, not before (RFC 0011 gate).
6. **Fix the spec, not just the code** — RFC 0012 amendments: `oofalse`→`oofalsify`, `oohash` pick, add `ooflash`, record `ooconsent`/`ooqueue`/`oonotes`/`oopdf`/`oomail` verdicts; delete phantom `unix_consolidation_blueprint.md` ref; scrub `website/llms.txt:35`, `oodocs/README.md:54` (`ooffice`→`oooffice`), 9 `ooagent-*` README lines, `oooda-engine` symlink docs, `northstar.oot` L4 list + `status` declaration, 6 `oofzf` AGENTS.md copies, hardcoded host bindings.
7. **Renames after ownership settles** (§6.5): apps → OS → kernel → agents → tools → core.
8. **Native-implementation debt** — `ooflash` shims → native `.oo`; 8 exec-relay persona tables → native impls tested **without** upstream binaries present; kill `oodac_cluster.sh`, `mcp_client.oo` fallback, `spawn.oo` aliases after renames land.
9. **Extract shared substrate** — apps 16× framework copies + kernel 15-page template + DE 28-file clone-set → `std` imports (Rule 1.25 §3); `std`→`std-hw` split; kernel template dedup.
10. **Hygiene & gates** — `link-law` gate in all cloud/agents Makefiles; `.ooda-cache` purge; `8`/`bracket_probe*` debris; `bin/`vs`dist/` convention; `install.sh` bare names; `oodac` stale copies; `SRC`-`fsprobe` rebuild defect; `ELF64` README lies; extend registry beyond L3 (catalog blindness is why C2 survived); page-gate allowlist for `boundary_257_lines.oo`; declare anchor-shim exemptions for the 246/1,857 core violations or schedule cleanup.

---

## 8. Residual risk — what no pass could establish

1. **No builds or tests were run by any of the three passes.** "Ready to archive" = source-structure readiness only; run `make all` on each host before deleting any absorbed repo.
2. **mcode's 82-token matrix** is equality-chain extraction; table-driven personas could evade it. Re-derive when building the Phase-1 registry.
3. **devin's 104-skeleton count** was sampled, not exhaustively classified (±104).
4. **The tree is live** — `ooflash` landed mid-audit (03:55–03:59 HST). Re-snapshot before executing Phase 5.
5. **`std/anchor.oo` vs `std/hw/anchor.oo`** contradict each other on whether `hw/` is docs-only — the split resolves it regardless.
6. **External install scripts** may reference `ooagent-*` applet names outside these trees — verify before scrubbing the 9 README lines.
7. **`/Projects/idlescreen`** (out of scope) contains `spotlight(s)` literals in ASCII scenes — will trip a naive hostname lint if applied repo-wide.

---

## 9. Audit quality assessment

| | mcode (788 lines) | devin (283 lines) |
|---|---|---|
| **Method** | token-collision matrix, machine-extracted | physical subtree graph + RFC conformance |
| **Strength** | complete quantification (82 tokens, 21 catalog), per-line citations, conformance sweep, deepest single defect (`std/hw`), only live code bug (port mismatch) | inversions vs RFC, name-semantics layer (cryptic names, ghosts, missing coverage), hygiene findings (oofzf copies, debris), skeleton-stub classification |
| **Blind spot** | name zoo, skeleton class, debris, `oosqllite` | `std/hw` (biggest scope violation), `oohash`↔`oob3sum` cycle, argv0-in-source, hardcoded IPs, catalog-collision enumeration |
| **Verified errata** | 3 cosmetic (17→16, 20→21, `ooshell` ghost) | 1 overstatement (`oowm`/`ooterm` "file-for-file") |
| **Reliability** | every sampled claim verified | every sampled claim verified |

The two passes are genuinely complementary: mcode is the **measurement** pass (counts, matrices, sweeps), devin the **spec-conformance** pass (RFC adjudication, name semantics, hygiene). Neither alone covers the defect space; together they do.

---

**Bottom line:** RFC 0012's consolidation is directionally right and partially implemented, but ownership was never enforced — so absorbed names are sold twice, canonical names exist only on paper, and four pairs of binaries point at each other. Publish the ownership table (step 1) **before** any archive or rename, or every fix re-creates the ambiguity it removes.

*Consensus produced by Devin `wR:p2`, reconciling `naming-audit-devin.md` (283 lines) against `naming-audit-mcode.md` (788 lines) with independent tree verification. Supersedes the earlier `wR:p1` draft of this file. Read-only; no builds/tests executed.*
