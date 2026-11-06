# Naming & Single-Responsibility Audit — Independent Findings (Devin)

> **Disposition (2026-11-06):** Independent pass 1 of 2 — subsumed by `naming-audit-consensus.md` (reconciled + tree-reverified). Findings landed via `persona-ownership.oot` + catalog `cb4490b`.


**Scope:** All repositories across the 9 openOODA organizations under `/Projects/` (read-only inspection only: directory names, `README.md`, `Makefile` `BIN`/`PERSONAS`, `.oo` page inventories, governing docs). No compilers, builds, or tests were executed.

**Date:** 2026-11-05 · **Auditor:** Devin (independent, zero-trust)

**Governing documents consulted:** `openOODA/rules.oot` (25 laws, esp. §1.19 naming, §1.25 zero-link), `rfcs/0012-unix-less-is-more-consolidation.oot` (377→129 plan + persona contract), `rfcs/0010` (fleet governance), `rfcs/0011` (validation), `northstar.oot` (layer model), `docs/tools-backlog.oot` (152-repo backlog table), `ZERO_SYMLINKS_DIRECTIVE.md`.

---

## 0. Executive Summary

The fleet is **mid-consolidation and diverged from its own RFC in both directions**: some repos are correctly absorbed and ready to archive, some RFC-canonical names do not exist at all, several absorptions landed in semantically wrong hosts or in *two hosts at once*, and at least three absorbed-vs-canonical relationships are **inverted between code and RFC** (`oomail`, `oocoder`, `oodeploy`/`oobuild-fleet`). Repo/dir names are almost universally consistent with `BIN` names (zero `BIN`≠dir mismatches found), but ~1 in 6 names are cryptic, colliding, typo'd, or duplicated across layers. The deepest structural issue is not any single bad name — it is that **most repos are clones of one shared capability-substrate template with 1–5 domain pages of actual identity**, so "repository count" overstates "product count" roughly 10–20× in L2/L4/L5/L6/L7.

Severity-ordered headline findings:

| # | Finding | Severity |
|---|---|---|
| F1 | Consolidation direction inverted vs RFC 0012 in ≥3 pairs (oomail→oochat, oocoder→ooreviewer, oodeploy↔oobuild-fleet) | **Critical** |
| F2 | Same persona embedded in **two different canonical hosts** (oodns-cloud, ooqueue, ooclip, ooshot, ootaskmgr, ooarchitect, oohealthd) | **High** |
| F3 | RFC-canonical repos that **do not exist**: `oooffice`, `ooauthd`, `ooboot`, `oohal`, `oodrv-{storage,io,virt}`, plus doc-named `oocodec`, `ootext`, `oozip`, `oocage` | **High** |
| F4 | `oosqllite` is a committed typo (upstream `sqlite3`); `oote` squats the `tee` namespace while meaning "theming engine" | **High** |
| F5 | Systemic substrate cloning: L4/L5 repos are ~27 identical capability-demo pages + 1 domain page; DE repos `oowm`/`ooterm` are file-for-file identical trees | **High** |
| F6 | Doc drift: RFC vs `northstar.oot` disagree on canonical sets (L4 especially); repo counts drift (4/5/6 meta, 10/11/9 core) | **Medium** |
| F7 | `oooda-engine` docs advertise persona **symlink** applets (`bin/ooplanner`, `bin/ooarchitect`), contradicting §1.25; cloud+agents lack the `link-law` Makefile gate entirely | **Medium** |
| F8 | 104 of 258 tools are one identical 13-file "file-grep skeleton" stub whose READMEs all claim "Native X TOOL" — misleading product claims at fleet scale | **Medium** |
| F9 | Six shipped tools carry a stale `oofzf` `AGENTS.md` (wrong repo name, wrong domain table) | **Low** |
| F10 | Workspace debris: `/Projects/openOODA/8` scratch file, `openOODA-DE/bracket_probe*.txt`, 385 `.ooda-cache/` residue dirs | **Low** |

---

## 1. Method & Evidence Base

- Enumerated every `*/` under all 9 orgs: **378 product subdirectories + 1 stray file + 2 stray probes + 1 docs-site repo** (`openOODA-tools.github.io`).
- Per repo, extracted: `README.md` H1/tagline, `Makefile` `BIN`, `PERSONAS`, presence/shape of `persona/` or `personas/`, `.oo` file inventory, and "Absorbed" banner markers.
- Verified absorption claims by checking for physical persona subtrees (`<host>/<absorbed>/`, `persona/<name>/`, `core/persona/<name>/`) rather than trusting README text.
- Skeleton-stub detection: repos matching the uniform `cli.oo + read.oo + core/{cap,codec,engine,ring,table}.oo` relay template.
- Cross-checked every canonical name in RFC 0012 §2.3 and `northstar.oot` §1.1 against on-disk dirs (ghost-name test).

**Zero `BIN` mismatches:** every Makefile `BIN` matches its directory name (`dist/` in L0+L3, `bin/` elsewhere — a minor convention inconsistency). **Zero symlinks/hardlinks on disk** (§1.25 holds physically).

---

## 2. Category 1 — Naming Mismatches & Misleading Names

### 2.1 Concrete name defects (repo/binary level)

| Name | Problem | Evidence |
|---|---|---|
| `oosqllite` | **Typo**: upstream is `sqlite3`; correct form is `oosqlite`. Typo is committed across dir, `BIN`, and `AGENTS.md`; its `README.md` is 0 bytes | `tools/oosqllite/` |
| `oote` | Squats the `tee` namespace but is the **openOODA Theming Engine** (96 pages). No `ootee` exists; `tee` is uncovered. Any reader/batch script reading `oote` will expect `tee(1)` | `tools/oote/README.md` |
| `oonaa` | Cryptic acronym ("NO AMBIENT AUTH" capability checker). Undiscoverable | `tools/oonaa/` |
| `ooripl` | Cryptic acronym ("INTERACTIVE REPL"); overlaps `oosh`'s REPL role | `tools/ooripl/` |
| `oobiew` | Upstream-derived (BIEW hex viewer) but collides visually with DE `ooview`; reads as a typo | `tools/oobiew/` |
| `oobound` vs `ooboundary` | Near-identical names, different domains (runtime bounds vs network egress). Indistinguishable | `tools/oobound*/` |
| `oocsplt` | Truncated `csplit` (expected `oocsplit`); asymmetric vs `oosplit` | `tools/oocsplt/` |
| `ooss`/`oossh`/`oossl` | Three one-letter-apart names (`ss`, `ssh`, `openssl`) — maximal typo hazard | tools |
| `oood` | `od` octal dumper; reads as `oooda`/`oooda-engine` prefix collision | `tools/oood/` |
| `oomeminfo` | Upstream is `free`, but `oofree` also exists — two repos claim the same memory-report domain | tools ×2 |
| `ootls`/`oossl` | **Both declare upstream `openssl`** — duplicated parity contract for one upstream tool | tools ×2 |
| `oofilter` | "Native AWK Drop-In" while `ooawk` ("RECORD PROCESSOR") also exists — two AWKs | tools ×2 |
| `ooimage` | Sounds like an image viewer; is the **OS image builder** (containers, `ooda_buildbox` tiers) | `OS/ooimage/` |
| `oomenubar` | DE-concept name living in L3 tools; it is a terminal status bar, overlaps `oopanel` | `tools/oomenubar/` |
| `oorev` | `rev` line-reverser; name implies "revision/revocation" in a capability system | `tools/oorev/` |
| `openOODA-tools.github.io` | Docs-site repo inside a product org (necessary GitHub convention, but it breaks the `oo*` uniform namespace and inflates repo counts in docs: 256/257/258) | tools |

### 2.2 Doc-canonical names that don't exist (ghost names)

Referenced as canonical in governing docs or READMEs but **no repo exists**:

- `oooffice` — RFC 0012's L5 office-suite host. The actual suite consolidator is **`oodocs`** (real personas `oosheet`, `oodeck`, `oonotes`, `oopdf` implemented under `oodocs/personas/`).
- `ooauthd` — RFC's L2 auth daemon. The actual session/policy merge landed as `oosession` ⊃ `policy/`.
- `ooboot`, `oohal`, `oodrv-storage`, `oodrv-io`, `oodrv-virt` — RFC's L1 canonical set. Reality kept `ookernel-*`/`oodrv-*` names and did *different* pairwise absorbs (§4).
- `oocodec`, `ootext` — named in `ZERO_SYMLINKS_DIRECTIVE.md` as consolidated canonical tools; the actual repos remain `oobase32/58/64` and `oosort`+text family.
- `oozip` — listed in RFC 0012 §2.2.4 archive family; only `oounzip` exists (unzip with no zip producer).
- `oocage` — `ooaid` README names it as the GPU-cell runner tool; no such repo exists anywhere.
- `oowhich`, `ooide`, `oomsg`, `ooidle`, `ooscreensaver` — persona tokens only (legitimate under RFC's "persona is a token, not a file" rule, but they inflate the namespace in docs without any marker saying *token-only*).

### 2.3 Layer/role labels that lie

- **`oollama`** README calls itself "Layer 4 (`openOODA-tools`)" — tools is **L3**, not L4; it is also absorbed into `ooaid` (**L2**), so a single README spans three wrong/right layer claims.
- Skeleton stubs (104 repos) uniformly claim "**Native X TOOL**" while shipping a file-grep skeleton that relays unknown argv upstream. `ooip show <file>` greps a file; it does not run `ip`. The READMEs present vapor capability as shipped product — misleading names *of function*.
- `oorealm`/`oosvc-mgr`/`ooimage`/`ooinit` READMEs badge "Layer: `os` on `openOODA-core` (L0)" — the repos live in the L2 OS org; the "on L0" phrasing is confusing but internally consistent (built on L0).

### 2.4 Stale `AGENTS.md` copies

Six shipped tools carry `oofzf`'s house-laws file verbatim — wrong repo name, wrong capability matrix (`FsReadCap/EnvCap` only), wrong domain table (`score/`, `ui/`, `render/`, `ipc/` + `packaging/oofzf.spec`):
`ooclock`, `oocurl`, `oops`, `oosed`, `ootar`, `ootree`.
(`oocurl` literally says "Every agent operating on `oofzf` MUST comply".)

### 2.5 `BIN`/`dist` convention split (minor)

`openOODA-core` and `openOODA-tools` emit to `dist/`; kernel, OS, DE, apps, cloud, agents emit to `bin/`. Not a violation, but an inconsistent install contract — the Binary Parity Law (`~/.openooda/bin/<tool> == dist/<tool>`) only literally names `dist/`.

---

## 3. Category 2 — Scope Pollution / Single-Responsibility Violations

### 3.1 The systemic one: substrate-clone repos

The dominant SRP violation is architectural, not per-name. Across L2/L4/L5/L6/L7 most "products" are **the same capability-substrate demo payload** (capability register, Byzantine quorum, Merkle audit chain, blackbox recorder, speculative transactions, warrant/delegate/revoke, PQC seal) + a thin domain veneer:

- **L5 apps**: every repo ≈ 27 identical pages (`core/{blackbox,capreg,engine,persist,quorum,share,speculate,state}`, `sec/{audit,delegate,pqcseal,revoke}`, `ipc/{framebuf,payload,wayland_client}`, 8 `tests/*`, `ui/view.oo`) + **exactly one domain page**: `oomail→mbox.oo`, `oonotes→stats.oo`, `oopdf→info.oo`, `oosheet→query.oo`, `oodeck→slides.oo`, `oopaint→info.oo` *(same filename as oopdf's)*, `oogit-ui→refs.oo`, `oochat→chatlog.oo`, `oomedia→probe.oo`. ≈90% boilerplate / 10% product.
- **L4 DE**: `oowm` and `ooterm` have **file-for-file identical trees** (28 files: same `core/{attest,audit,blackbox,cap,codec,consensus,delegate,engine,rect,revoke,ring,share,speculate,table}` + same 8 tests). Product identity lives invisibly *inside* `engine.oo`/`table.oo`.
- **L3 stubs**: 104 repos share one 13-file skeleton (`cli.oo`, `read.oo`, `core/{cap,codec,engine,ring,table}.oo`, `qa/parity/*`, `tests/test_main.oo`) where the only real verb is "grep this file; relay unknown argv to upstream".
- **L6 cloud**: `ooqueue` vs `ooconsent` share ~28 of ~36 pages; domain difference is ~4 pages each.
- **L2 OS daemons**: uniform `core/{capreg,machine,parse,policy,store,types,warrant,wire}` + `hw/*` skeleton; README one-liners ("X table that…") admit they are bounded state machines, not daemons.

**Audit verdict:** the RFC's own diagnosis (1,079 duplicated harness pages) is confirmed and ongoing. These repos violate the *spirit* of single responsibility: the repo name promises a product; the tree delivers a shared demo substrate. Before any archive/split decision, decide whether the substrate becomes one shared `std/` import surface (the law already says code sharing via `import "std/..."`, not copies).

### 3.2 Repo-level multi-domain scope

- **`oofiles`** absorbed `ooview` (doc viewer), `ooedit` (text editor), `ooclip` (clipboard broker), `ooshot` (screenshot), `ootaskmgr` (task manager) — a *file manager* now serving five unrelated desktop domains. Legally multi-call; semantically a kitchen sink. `ooportal` is the more defensible host for `ooclip`/`ooshot` (FrameCap-gated) — and indeed **also** embeds them (see F2).
- **`oocockpit`** (absorbed into `oopanel`) embeds `ooagent-hud` (RFC-canonical!) + `ootaskmgr` — a nested shell-inside-a-shell carrying a canonical product.
- **`oochat`** carries a fuller mail implementation (`personas/oomail/{engine,mbox,persist}`) than the standalone `oomail` repo (`mbox.oo` only). Two divergent mail impls exist; the non-RFC one is bigger.
- **`oocat`** — "file viewer and pager" = `cat` + `less` + syntax highlighting; triples its Unix mandate.
- **`ooclock`** — TUI matrix clock + stopwatch + pomodoro; three domains.
- **`ooenv`** — env controller + secret sanitizer + exec simulator.
- **`ooaid`** — inference daemon that also absorbed the `oollama` CLI client (L3 tool inside an L2 daemon — cross-layer scope, though defensible as client+server pair) and references nonexistent `oocage`.
- **Kernel pairwise absorbs**: `oodrv-net` ⊃ `oodrv-pci`+`oodrv-usb-hid` personas (a *network* driver serving PCI-bus and USB-HID personas); `ookernel-sched` ⊃ `ookernel-mm`+`ookernel-ipc` (scheduler serving MM+IPC). Technically fine as personas, semantically arbitrary — the RFC's `oodrv-{storage,io,virt}` grouping is the correct domain shape and was not followed.
- **`oomedia`** — the user's example is **verified remediated**: README documents the flasher was extracted to `ooflash` (real 17-page dedicated repo with devlock/digest/rawio/verify); zero flash/usb residue in `oomedia`. *But* `ooflash` is absent from RFC 0012's L5 canonical list — the doc never caught up to the correct split.

### 3.3 Org-boundary (cross-layer) leaks

- `omenubar` (terminal status bar — a DE chrome concept) sits in tools while `oopanel`/`ooborder` cover the same visual role.
- `ooherdr` (agents) ships an `oomux` persona — terminal multiplexer while `ootmux`+`ooscreen` exist in tools.
- `mcp` naming appears at three layers: `core/mcp` (server), `tools/oomcp` (gateway/router), `tools/oomcprun` (task runner).
- DNS exists at three layers: `tools/oodns` (resolver), `OS/oodnsd` (caching resolver), `cloud/oodns-cloud` (DNS service) — plus 3 more lookup clients `oodig`/`oohost`/`oonslookup` in tools.
- Sessions: `OS/oosession`, `tools/oologinctl` (upstream: loginctl — same domain), `tools/ooscreen`+`ootmux` (session detach).
- Power: `tools/{oopower,ooreboot,ooshutdown}` vs `OS/oopowerd`.
- `oomenubar`, `oonotify` vs `DE/ootoast`; `tools/oofile` vs `DE/oofiles` vs `OS/oofs-*`; `tools/ooguard` vs `agents/oogovern`.

---

## 4. Category 3 — Ambiguous, Redundant & Colliding Names

### 4.1 Duplicate embedding (same name, two canonical hosts) — **the sharpest defect**

| Persona/repo | Host 1 | Host 2 | Note |
|---|---|---|---|
| `oodns-cloud` | `oomesh` (RFC-correct) | `oogateway` | DNS embedded in *both* L6 edge hosts |
| `ooqueue` | `oodb-dist` | `oosched-cloud` | Queue lives in DB *and* scheduler |
| `ooclip` | `oofiles` | `ooportal` | Clipboard in file manager *and* portal |
| `ooshot` | `oofiles` | `ooportal` | Screenshot in both |
| `ootaskmgr` | `oofiles` | `oocockpit` | …and oocockpit itself is absorbed into oopanel |
| `ooarchitect` | `oogovern` | `oooda-engine` (`persona/architect.oo`) | Architect in two L7 hosts |
| `oohealthd` | `ooinit` (`healthd/` subtree) | standalone repo still ships | Dual existence, not marked absorbed |

These are not personas-by-design (a persona is a token inside ONE binary); they are **copied subtrees in two repos**, i.e., forked sources of truth that will drift.

### 4.2 Inverted absorptions (code contradicts RFC)

| Pair | RFC 0012 says | Code does |
|---|---|---|
| `oomail`/`oochat` | `oomail` canonical; `oochat` dropped | `oomail` marked **Absorbed → into `oochat`** |
| `ooreviewer`/`oocoder` | `oocoder` canonical; `ooreviewer` dropped | `ooreviewer` contains `oocoder/` (30 pages) |
| `oodeploy`/`oobuild-fleet` | `oodeploy` absorbs `oobuild-fleet` | both directions exist: `oodeploy`⊃fleet+infer+sched **and** `oobuild-fleet`⊃`oodeploy/` (32 pages) |
| `ooagent-hud`/`oocockpit` | `ooagent-hud` canonical; `oocockpit` dropped | `oocockpit` embeds `ooagent-hud` (while cockpit itself → `oopanel`) |
| `oonotes`/`oopdf` | canonical standalone | also personas inside `oodocs` (dual existence) |

### 4.3 Redundant/overlapping families (intra-layer)

- **Diffs (11)**: `oodiff, oodiff3, oocmp, oocomm, oosdiff, oowdiff, oobindiff, oogitdiff, oosemantcdiff, ooschemadiff, oostructureddiff, ooastdiff` — RFC folds 6 into `oodiff`; the *diff suffix zoo* remains 4 overlapping "semantic" differ names.
- **Digests (8)**: `oohash, oob3sum, oochecksum, oocrc32, oosha256, oosha512, oomd5` (+`oocksum` persona token). `oochecksum` vs `oohash` unmapped overlap.
- **Arch/compress (9)**: `ooarchive, ootar, oo7z, oocpio, oounzip, oogzip, oobzip2, ooxz, oozstd` (+ghost `oozip`).
- **Net admin (~20)**: `oocurl/oowget/oowget2/oofetch`, `oonetcat/oosock/ooss/oonetstat`, `ooip/ooifconfig/ooarp/ooroute`, `ooiptables/oonftables/oofirewall`, `ooping/oomtr/ootraceroute`, `oodig/oohost/oonslookup/oodns/oowhois`, `ooscp/oosftp/oossh/ootunnel/oorproxy`. Three firewalls, four DNS lookups, three iface tools.
- **Sandbox/security (~18)**: `oocap/oolandlock/ooseccomp/ooapparmor/oochroot/oocgroup(+v2)/ooguard/oosandbox/oonaa/oonegatrust/oopolicy/ootaint` vs `OS/oorealm` vs `tools/ooaudit/ooattest/ooprovenance`.
- **Sign/crypto (~10)**: `oosign/ooverify/oocert/ookeygen/oovault/ootoken/oossl/ootls/oossh/oonegatrust` — `oossl`≈`ootls` (same upstream).
- **TUI widgets (~19)**: `ooansi/oocolor/oorgb/oohsl/oogradient/oote/oopreset/ooglyph/oofigure/ooborder/ootable/oobanner/oosparkline/oobar/ooprogress/oospinner/oodialog/oomenubar/ooprompt` — 3 progress bars (`oobar/ooprogress/oosparkline`), 4 color tools.
- **Monitoring (~16)**: `oowatch/ooswatch/oomonitor/ootop` (4 watchers!), `ooiostat/oompstat/oovmstat/oosensors`, `oohwinfo/oolshw/oolspci/oolsusb/oocpuinfo`, `oomeminfo/oofree`, `oodf/oodu`, `oodmesg/oojournal`.
- **Pagers/viewers (7)**: `ooless/oomore/oocat/oohex/ooxxd/oobiew` + `DE/ooview` + `apps/oopdf`.
- **Agents overlap**: `oorouter`≈`ooherdr` (both score capability-masked agents by load and dispatch); `ooredteam`≈`oofalsify` (both adversarial boundary generators); `ooarchitect`≈`oogovern`≈`oorelease` (all audit VERSION/ooda.pkg/LICENSE/ci.yml); `ooplanner`≈`oooda-engine` (both import-graph→build-order).
- **Scheduler collisions across layers**: `tools/{ooat,oobatch,oocron,ooworker}` vs `cloud/oosched-cloud` vs `kernel/ookernel-sched` — "sched" means 3 unrelated things.
- **`oosession`/`ooscreen`/`ootmux`/`oologinctl`/`ooworker`** — session/mux/process cluster blurs layers.

### 4.4 Missing coverage (naming gaps)

No repos for core tools the fleet otherwise duplicates: `oodate`, `oodd`, `ooecho`, `oocal`, `ooed`, `oowhich` (persona-only), `ootee` (name squatted by `oote`), `oozip`. `ooflash`'s `rawio.oo` wraps host `dd` because **no `oodd` exists** — an ironic gap for a stack that otherwise reimplements everything.

---

## 5. Category 4 — Keep / Rename / Split / Archive Verdicts

### 5.1 READY TO ARCHIVE (absorption implemented & banner-marked)

| Repo | Absorbed by | Evidence |
|---|---|---|
| `tools/oollama` | `OS/ooaid` | README "Absorbed… archived"; `ooaid/ollama/` impl exists |
| `apps/oodeck`, `oosheet`, `oonotes`, `oopdf` | `apps/oodocs` | Banner-marked; `oodocs/personas/{oodeck,oosheet,oonotes,oopdf}/` impls exist — **but** RFC lists oonotes+oopdf as canonical: reconcile before archiving |
| `apps/oomail` | `apps/oochat` | Banner-marked; `oochat/personas/oomail/` impl — **inverted vs RFC** (resolve F1) |
| `apps/oopaint` | `apps/oocanvas` | PERSONAS impl present |
| `apps/oogit-ui` | `apps/oostudio` | PERSONAS impl present |
| `OS/oodnsd` | `OS/oonetd` | `oonetd/dns/` subtree (8 pages) |
| `OS/oopolicyd` | `OS/oosession` | `oosession/policy/` subtree |
| `OS/oopowerd` | `OS/oodevd` | `oodevd/power/` subtree |
| `OS/oosvc-mgr` | `OS/ooinit` | `ooinit/svcmgr/` subtree |
| `OS/oofs-ext4`, `oofs-tmp` | `OS/oovfs` | `oovfs/{ext4,tmp}/` subtrees |
| `cloud/{oocdn}` | `oogateway` | embedded; **but also dup'd inside `oomesh`? no — `oodns-cloud` is the dup; oocdn only in gateway** |
| `cloud/{oobuild-fleet,ooinfer-grid,oosched-cloud}` | `oodeploy` | subtrees in `oodeploy/` — *but see F1/F2 reverse+dup embeddings* |
| `cloud/{oostore-cas,ooregistry-cloud}` | `oostore` | subtrees in `oostore/` |
| `cloud/{oodns-cloud,oorelay}` | `oomesh` | subtrees in `oomesh/` — `oodns-cloud` is **dup'd in `oogateway`** (resolve first) |
| `cloud/{ooconsent}` | `ooidentity` | subtree in `ooidentity/` (RFC-silent; sensible fill) |
| `cloud/{ooqueue}` | `oodb-dist` | subtree in `oodb-dist/` — **also in `oosched-cloud`** (resolve F2) |
| `DE/{oowm,oowall}` | `oocomp` | `oocomp/core/persona/{oowm,oowall}/` |
| `DE/{ooview,ooedit,ooclip,ooshot,ootaskmgr}` | `oofiles` | `oofiles/core/persona/*` — `ooclip`/`ooshot`/`ootaskmgr` **dup'd** (resolve F2) |
| `DE/{oocockpit,oolaunch,ooshelf,ootoast}` | `oopanel` | `oopanel/core/persona/*` |
| `agents/{ooarchitect,oorelease}` | `oogovern` | subtrees present |
| `agents/{ooredteam}` | `oofalsify` | subtree present |
| `agents/{ooeval,ooevolve}` | `ooconsensus` | subtrees present |
| `agents/{ooplanner,ooarchitect}` | `oooda-engine` | `persona/{planner,architect}.oo` — `ooarchitect` **dup'd** with oogovern |
| `kernel`: per persona tables | see below | registry-level personas (`absorbed_set.oo`), no full subtrees — **not** ready until domain impls are actually ported |

**NOT ready to archive:** the 104 skeleton stubs in tools (they are *unimplemented*, not *absorbed* — backlog work, keep on the backlog board); `oonotes`/`oopdf`/`oomail`/`oohealthd`/`oolock`/`ooagent-hud`/`oodeploy`-in-fleet until duplicate-embedding and RFC-inversion verdicts are made; anything whose "absorption" is only a `persona/absorbed_set.oo` registry entry with no ported domain logic (kernel set, parts of OS).

### 5.2 KEEP (canonical hosts, correctly named)

`core`: all 9 (`cli ooda oodac oodar opm lsp mcp std tui`) — clean N-binary roles per §1.14.
`tools`: ~64-canonical set is right in shape: `oosh, oogrep, oofind, oojq, oocurl, oodiff, oob3sum, ootar/ooarchive, oosh(via oosh personas), oote? (rename), ootop, ools, oocat, ooless, oosort, oosed, ooawk…` plus `oowatch` (keep — pick over `ooswatch`).
`OS`: `ooinit, oovfs, oonetd, oosysbus, oohealthd(or fold into ooinit as it already is), ooimage, ooaid` (+ `oosession`→rename `ooauthd`).
`DE`: `oocomp, oofiles, oopanel, ooportal, ooterm, oosettings, oolock, oobazaar, ooagent-hud` — matches RFC's 9 (implementation confirms).
`apps`: `oobrowser, oostudio, oodocs→rename, oocanvas, oomedia, oodaw, oopdf?, oomail?, oopass, oovm-ui, ooflash` (+`oochat` vs `oomail` decision).
`cloud`: `oomesh, oostore, oodeploy, oogateway, ooidentity, oodb-dist, ootelemetry, oobilling` (+`ooqueue` either canonical or committed to `oodb-dist`).
`agents`: `oooda-engine, ooherdr, ooquota, oofalsify, ooconsensus, oocoder, oomemory, oogovern` (+resolve `ooreviewer`/`oocoder` inversion, `oorouter` vs `ooherdr` overlap).

### 5.3 RENAME candidates

- `oodocs` → **`oooffice`** (it is the office suite; "docs" undersells sheet+deck+pdf; aligns with RFC).
- `oosession`(+`policy/`) → **`ooauthd`** (RFC name; session+policy is the auth daemon).
- `ookernel-boot` → **`ooboot`**; `ookernel-hal-{x86,arm64,riscv}` → **`oohal`** (one repo, arch personas); `oodrv-{nvme…}` → **`oodrv-storage`**; `oodrv-{display-gop,usb-hid…}` → **`oodrv-io`**; `oodrv-{virtio,pci?}` → **`oodrv-virt`** — i.e., implement the RFC's L1 naming instead of today's arbitrary pairwise absorbs.
- `oosqllite` → `oosqlite` (or fold into `ooquery`/db persona).
- `oote` → keep function, consider `ootheme` (releases the `tee` namespace); or accept squatting + add `ootee`/`tee` persona under `oocat`.
- `oobiew` → `oohexview`? (or persona under `oohex`/`ooxxd`); at minimum disambiguate from `DE/ooview`.
- `ooboundary`/`oobound` → merge to one name (`oobound`) with `egress` persona.
- `openOODA-tools.github.io` — GitHub-forced name; document it as non-product in `northstar` to fix the 257-vs-258 count drift.

### 5.4 SPLIT candidates

- **`oodocs`**: if `oochat` precedent (fat multi-persona app binary) is unloved, split `oosheet`/`oodeck` impls back out — but the cleaner verdict is *rename, don't split*.
- **`oofiles`**: split `ootaskmgr`+`ooedit` personas out of the file manager OR move `ooclip`/`ooshot` to `ooportal` permanently (dedupe F2) and let `oofiles` keep `ooview`/`ooedit` as preview/open-with personas.
- **`oocat`**: split pager half into `ooless` (or keep as `oocat view` subcommand — acceptable).
- **`oocockpit`**: after absorbing into `oopanel`, its embedded `ooagent-hud` subtree must move to the canonical `ooagent-hud` (reverse the embedding).
- **`oobuild-fleet`**: remove its embedded `oodeploy/` subtree — single source lives in `oodeploy`.
- **tools data family**: `oofilter`→merge into `ooawk`; `ootls`→merge into `oossl`.
- **`oostructureddiff`/`oosemantcdiff`/`ooschemadiff`/`ooastdiff`/`oogitdiff`**: collapse to one `oostructureddiff` host with format personas (ast/schema/semantic/git).

### 5.5 RFC/text amendments required (doc-law drift)

1. RFC 0012 L7 list says **`oofalse`** — almost certainly `oofalsify` (a tools↔agents name collision *inside the RFC itself*). Fix the RFC.
2. RFC L4 list vs `northstar.oot` L4 list disagree (`oosettings`+`oolock` vs `oowm`+`oocockpit`); implementation matches the RFC — update `northstar`.
3. Add `ooflash` to the L5 canonical list; decide `oochat`-vs-`oomail` canonical direction (code picked `oochat`; RFC picked `oomail` — pick one, prefer `oomail` as host name with `oochat` persona since "mail" is the superset domain).
4. Record `ooconsent→ooidentity`, `ooqueue→oodb-dist` decisions in the RFC mapping (implementation chose them; doc never did) — and kill the `oosched-cloud`/`oogateway` duplicate embeddings.
5. Declare `status` a meta-org repo in `northstar` (it's a real repo; doc says 4–5).
6. Reconcile core count (9 dirs vs doc claims of 10–11) and tools count (257 vs 258 incl. the github.io repo).
7. `oooda-engine` §4.1 advertises persona symlink applets — scrub the doc (no recipe found in Makefile, but `make build` text says it installs `bin/ooplanner`/`bin/ooarchitect` symlinks; §1.25 forbids them as files; install the `link-law` gate in all 16 agents + all 18 cloud repos — currently absent there).

---

## 6. Per-Org Verdict Table

| Org | Repos now | Canonical target | State | Verdict |
|---|---|---|---|---|
| @openOODA (meta) | 6 (+`8`, +debris) | 5–6 | `status` undocumented; `catalog` carries `caps`/`echo`/`hello` non-oo fixture packages | KEEP all; document `status`; sweep debris |
| core (L0) | 9 | 9 (docs: 10–11) | Cleanest org; names honest (`oodac`/`oodar`/`cli`/`ooda`/`opm`/`lsp`/`mcp`/`std`/`tui`) | KEEP |
| kernel (L1) | 16 | 6 | Names=dirs fine; absorptions are ad-hoc pairwise (net⊃pci+usb-hid; sched⊃mm+ipc; pci⊃virtio; boot⊃unikernel; mm⊃iommu), none of RFC's `ooboot`/`oohal`/`oodrv-*` names exist | **SPLIT/RENAME per RFC**; un-nest the pairwise absorbs |
| OS (L2) | 18 | 8 | Real subtree absorbs done (init⊃{healthd,svcmgr}, vfs⊃{ext4,tmp}, netd⊃dns, session⊃policy, devd⊃power); stragglers: `ooaudiod`, `oologd`, `oorealm`, `oosysbus`(host), `oohealthd` dual-exists; `ooauthd` ghost | Mostly on-track; dedupe `oohealthd`; decide `ooauthd` rename; home `ooaudiod`/`oologd`/`oorealm` (→`oosysbus`/`oohealthd`/`ooimage`?) |
| tools (L3) | 258 | 64 | 104 shipped + 104 skeleton stubs + ~50 partial; name zoo is worst in ecosystem (see §3.3–4.4); `oocurl` is the model consolidator (real `persona/` impl) | Aggressive merge per RFC persona tables; fix `oosqllite`/`oote`/dup families; stubs stay backlog, not "archive" |
| DE (L4) | 20 | 9 | Canonical-9 confirmed in code; hosts carry persona subtrees; 3 dup embeddings (ooclip/ooshot/ootaskmgr); `oocockpit` nests canonical `ooagent-hud` | KEEP 9; dedupe; disassemble `oocockpit` |
| apps (L5) | 17 | 11 | oomedia✓clean; `ooflash` real but unlisted; `oodocs`=de-facto `oooffice`; `oomail`/`oochat` inverted; `oonotes`/`oopdf` dual-exist | RENAME `oodocs`→`oooffice`; pick mail/chat direction; archive marked repos after verdicts |
| cloud (L6) | 18 | 8 | All 8 canonical exist + all absorbs embedded; BUT `oodns-cloud` & `ooqueue` dup'd, `oobuild-fleet`⊃`oodeploy` reverse-embed; `link-law` gate absent everywhere | KEEP 8; dedupe oodns-cloud→oomesh, ooqueue→oodb-dist; strip `oodeploy/` from `oobuild-fleet`; add gates |
| agents (L7) | 16 | 8 | Absorbs embedded; `oocoder` inverted into `ooreviewer`; `ooarchitect` dup'd (oogovern + oooda-engine); `oorouter`/`ooherdr` unmerged overlap; `oogovern`/`ooarchitect`/`oorelease` triple-overlap; RFC typo `oofalse` | KEEP 8; un-invert `oocoder`; fold `oorouter`→`ooherdr`; fix RFC typo; add gates |

---

## 7. Appendix — Hygiene & Residuals

- `/Projects/openOODA/8` — stray table-header scratch file at org root (REPO/FNLEN/FNS/HAS_SHAPE/LINKLAW/SIZE_BASELINE header, no data).
- `/Projects/openOODA-DE/bracket_probe.txt`, `bracket_probe2.txt` — identical bracket-probe scratch files at org root (outside any repo).
- `.ooda-cache/` residue: **385 dirs** across the fleet despite RFC Phase-1 purge item.
- Zero symlinks/hardlinks on disk (find -type l = 0) — §1.25 physically holds; the hazard is doc'd intent (oooda-engine applet symlinks) and missing gates (cloud, agents).
- `catalog` contains non-`oo` fixture packages (`caps`, `echo`, `hello`) — acceptable as fixtures, flag for namespacing clarity.
- `oosqllite` (and ~12 other skeleton repos) ship **empty or title-less READMEs** — no product identity at all.

*End of independent findings. Reconciliation against `naming-audit-mcode.md` lives in `naming-audit-consensus.md`.*
