# OODA (any repo)

**Location:** `~/OODA.md`  
**Scope:** Any codebase.  
**Purpose:** One rotation: **Observe → Decide → Act → Lock → Ship**.

**Always load:**
- `~/RULES.md` (axioms + plain English for the owner)
- `~/SWARM.md` (how to use helper agents — **required every OODA run**)

**When claims need hostility:** `~/PROBE.md`.  
**Product vision:** boards `DESIGN.md` or `ROOT/DESIGN.md` if present.

---

## Always on (from RULES — summary)

- First principles + enough planning to act  
- E-M, honesty/fail-closed, security posture, reverse entropy  
- Immune tests, **hygiene**, line pressure ≤256 (or repo lock)  
- Power law: Decide ≤ **5**  
- **Plain English** to the owner (RULES §1.10)

Full text: **`~/RULES.md`**.

---

## Always on (from SWARM — summary)

**Every OODA run loads SWARM.** The loop does not skip it.

| Rule | Meaning |
|------|---------|
| **Right-size helpers** | Light work → light agents. Heavy design → heavy agents. |
| **Small ships** | Give each helper one tight job. Stop at goal or first hard fail. |
| **No debugger swarm** | If stuck, probe with simple tools. Do not spawn more agents to “fix” a stuck agent. |
| **Isolate overlap** | Two helpers must not edit the same files unless isolated (branch/worktree). |
| **Hostile check** | A helper may attack claims (edge cases). On a real fail-open hole: trap closed, stop, report. |

Full text: **`~/SWARM.md`**.

**Solo is allowed** only when SWARM would waste effort (one tiny file, one command).  
Even then: you still **read** SWARM and **state** “solo under SWARM (reason).”

---

## Adapter (fill every session)

```markdown
ROOT:
Product binaries / how to build & run:
Backlog file (or issues):
Handoff file (e.g. SPRINT.md / PM.md):
Must-not-regress rails (discover under ROOT):
Hygiene commands (line lock, fmt, lint — if any):
ROOT/DESIGN.md or boards DESIGN present?:
SWARM plan: solo | fan-out (list roles + files each owns)
```

---

## 1. Observe

1. Handoff (PROGRESS / notes / SPRINT)  
2. Backlog (PM)  
3. **Tree health / hygiene snapshot** — line lock if present; obvious cruft; red rails  
4. Security-sensitive surfaces (auth, secrets, I/O, exec) if this product has them  
5. **SWARM skim** — is this turn multi-file / multi-role? Note fan-out or solo + why  

Ask: best next **product** step (E-M / information value)?  
Plan only enough to Act.

---

## 2. Decide (≤5)

Prefer, in order:

1. **Red product rails** / regressions  
2. **Honesty / security** fail-open holes  
3. **Next backlog item** (DESIGN-aligned)  
4. **DESIGN gap** → add to backlog, then do  
5. **Entropy / hygiene / split** only if blocking or cheap  

Also decide **SWARM shape** (mandatory output of Decide):

- **Solo** — one agent; reason fits SWARM (tiny / single file).  
- **Fan-out** — name ≤ few helpers; each owns **orthogonal** files or a pure read-only role (inventory, verify).  
- Never “many agents on one stuck bug.”

---

## 3. Act

- Implement on the **real** product path for this ROOT  
- Run Act **under the SWARM plan** from Decide (solo or fan-out)  
- Fail-closed unfinished work (or explicit residual)  
- Stay under line pressure or split same rotation  
- Ship tests with behavior when claims matter  
- Respect security posture (default-deny privileges; no secrets in tree)  
- Owner-facing notes stay **plain English** (RULES §1.10)

---

## 4. Lock (hygiene + rails)

**Hygiene is required here** (RULES §1.7), not deferred to PROBE:

1. **Execute Hygiene Check** — six steps from `RULES.md §1.7` (Line pressure, Cruft, Secrets, Temps, Git, Docs).  
2. **Product rails** — only scripts/CI this ROOT actually has (discover; don't invent).  
3. Backlog checkboxes only if **really** done (fixtures + product path).  
4. **SWARM Lock** — no leftover rogue helpers; no two agents left fighting the same files; verify claims yourself (RULES zero-trust agency).

If hygiene fails → do not Ship; fix or residual.

---

## 5. Ship

- Commit/push as appropriate (no secrets; no force-push of shared main unless owner policy)  
- Short report in **plain English**: what changed, why it matters, what is still not done  
- Note SWARM shape used: `solo (reason)` or `fan-out: roles…`  
- Prefer **reverse entropy**  
- **Never** auto-claim release/beta unless owner policy already did  

---

## When to run PROBE

Use **`~/PROBE.md`** in the same ROOT when:

- Security or privilege claims need falsification  
- You suspect fail-open, torn state, or synthetic green rails  
- After a large change to boundaries (I/O, auth, exec, caps)  

PROBE does **not** replace Lock hygiene; it **adds** hostility.  
PROBE workers still follow **SWARM** (no debugger swarms).

---

## Master prompt

```text
Run OODA from ~/OODA.md.
Always load: ~/RULES.md and ~/SWARM.md.
Target ONE repository ROOT. Fill the adapter (include SWARM plan).
Observe → Decide (≤5 + SWARM shape) → Act (under SWARM) → Lock (hygiene + rails + SWARM) → Ship.
Plain English to the owner. First principles, E-M, fail-closed, reverse entropy, security posture.
No soft-pass. No foreign product assumptions.
SWARM is automatic: solo only with a stated SWARM reason; else fan-out with orthogonal files.
For adversarial assumption hunt: ~/PROBE.md (still under SWARM).
```

---

## Product session notes (optional)

A short product pointer may set ROOT, DESIGN, backlog, and preferred rails only.  
Do **not** fork the whole OODA file per product.

---

*Process kit: **OODA** · **RULES** · **SWARM** · **PROBE**.*
