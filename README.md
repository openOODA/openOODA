<div align="center">

<pre>
   ____  ____  ___  ____    ___   ___  ____    _
  / __ \/ __ \/ _ \/ __ \  / _ \ / _ \|  _ \  / \
 / /_/ / /_/ /  __/ / / / | | | | | | | | | |/ _ \
/_____/ .___/\___/_/ /_/  | |_| | |_| | |_| / ___ \
      /_/                   \___/ \___/|____/_/   \_\
</pre>

### openOODA — Sovereign Systems Language for the AI Era

[openooda.org](https://openooda.org) · [Docs](https://openooda.org/guide/) · [Registry](https://registry.openooda.org/)

</div>

---

## What is openOODA?

openOODA is an AI-native, capability-secure systems programming language built for
sovereign software synthesis. The compiler verifies source code ahead-of-time, every
side effect requires an explicit unforgeable capability token, and functions declare
verifiable contracts (`requires`, `ensures`, `spec`).

Three design forces govern every line:

- **Subtractive optimization** — improve systems by removing drag, ambient authority,
  null pointers, and dynamic dispatch.
- **Boyd's E-M invariant** — `E-M = ((T − D) / W) * V`. Maximize thrust, eliminate
  drag, strip weight, accelerate velocity.
- **Deterministic execution** — bit-identical binaries, zero-timestamp digests, linear
  arena memory with O(1) bulk resets.

## Install

```sh
# 1. Install the ooda toolchain (compiler + runtime + driver)
curl -fsSL https://openooda.org/install.sh | bash

# 2. Add the standard library
opm install openOODA/std
```

## The 9-Repo Polyrepo

| Layer | Repo | Purpose |
|-------|------|---------|
| Strategic | [openOODA/openOODA](https://github.com/openOODA/openOODA) | Governance, RFCs, laws (this repo) |
| Operational | [openOODA/cli](https://github.com/openOODA/cli) | `ooda` workflow driver |
| Operational | [openOODA/lsp](https://github.com/openOODA/lsp) | Language server |
| Operational | [openOODA/mcp](https://github.com/openOODA/mcp) | Model Context Protocol server |
| Operational | [openOODA/opm](https://github.com/openOODA/opm) | Package manager |
| Tactical | [openOODA/std](https://github.com/openOODA/std) | Standard library (8 domains) |
| Tactical | [openOODA/ooda](https://github.com/openOODA/ooda) | Compiler + runtime monorepo |
| Meta | [openOODA/.github](https://github.com/openOODA/.github) | Org-wide profile & workflows |
| Meta | [openOODA/website](https://github.com/openOODA/website) | Website source |

The [Three-Layer Law](RULES.oot) (RULES.oot §1.23) holds the topology stationary:
governance changes never cascade into compiler rebuilds; compiler changes never alter
governance. `Δ_path = 0`.

## Onboarding (read in order)

1. **[ANCHOR.oo](ANCHOR.oo)** — strategic front door; the four-doc reading order.
2. **[RULES.oot](RULES.oot)** — the 23 laws. These do not change.
3. **[NORTHSTAR.oot](NORTHSTAR.oot)** — vision, grammar, AST, type system, 10 pillars,
   Gen 1–7 architecture.

## RFCs ([openOODA/rfcs/](rfcs/))

| # | Title | Status |
|---|-------|--------|
| [0000](rfcs/0000-template.oot) | Template | — |
| [0001](rfcs/0001-capability-security.oot) | Capability Security (14 tokens, zero ambient authority) | Implemented |
| [0002](rfcs/0002-design-by-contract.oot) | Design by Contract (`requires`, `ensures`, `spec`) | Implemented |
| [0003](rfcs/0003-file-format.oot) | File Format (Academy header, 256 cap, ASD-STE100) | Accepted |
| [0004](rfcs/0004-engineering-model.oot) | Engineering Model (3-layer architecture, E-M) | Accepted |
| [0005](rfcs/0005-tactical-subsystem-template.oot) | Tactical Subsystem Template | Accepted |

## Practices ([openOODA/practices/](practices/))

- **[8d-red-team.oot](practices/8d-red-team.oot)** — the 8 adversarial dimensions
  + 8-gate veto protocol.
- **[ooda-workflow.oot](practices/ooda-workflow.oot)** — the OODA loop, 5-component
  handoff, and multi-agent protocols.

## Core Capabilities

- **14 capability tokens** — `&FsReadCap`, `&FsWriteCap`, `&NetCap`, `&ProcessCap`,
  `&AllocCap`, etc. No token, no effect. No ambient authority.
- **256-line cap** — every `.oo`/`.oot` file ≤ 256 lines. One concept, one location.
- **Academy 4-Element Headers** — `# Title`, `Logline:`, `Setup:`, `Beats:` on every
  `.oo`; 2-line clean header on every `.oot`.
- **Multi-target emission** — direct ELF64, WASM, LLVM IR, or portable C99. No
  toolchain lock-in.
- **8-Dimensional Red Team** — adversarial verification with 8-gate blocking veto.
- **Generational Architecture** — Gen 1 (silicon) → Gen 7 (quantum swarm).

## License

Dual-licensed under your choice of [MIT](LICENSE-MIT) or
[Apache 2.0](LICENSE-APACHE). See [LICENSE](LICENSE) for details.

## Contributing

Open an issue, propose an RFC following [0000-template.oot](rfcs/0000-template.oot),
or join the [email list](https://openooda.org/).
