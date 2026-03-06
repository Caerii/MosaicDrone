# How to write and flesh out specs

↑ [Docs index](README.md)

Use this as a checklist when creating or improving a spec in `docs/`. The [docking interface](docking/interface.md) is a worked example.

---

## 1. Make the spec findable

- Put the spec in the right folder: `docs/<area>/<name>.md` (e.g. `docking/interface.md`).
- Add at the top: `↑ [Docs index](../README.md)` (adjust path if not one level under `docs/`).
- Ensure it’s linked from [docs/README.md](README.md) (Specs by area) and, if it’s a subsystem, from [subsystems/INDEX.md](subsystems/INDEX.md).

---

## 2. Clarify scope

- **Purpose**: One or two sentences on what the spec defines.
- **Scope / out of scope**: What this doc covers and what it doesn’t (with links to other specs). Reduces overlap and confusion.

---

## 3. Turn bullets into structured content

- **Requirements**: Use a table (Requirement | Target) so values are easy to scan and review.
- **Interfaces**: Add explicit pinout, message fields, or API tables instead of only prose.
- **Dimensions / envelope**: If relevant, add a small table (e.g. mating face, depth, ratings).

---

## 4. Add thresholds, timeouts, and recovery

- For state machines or sequences: table of **Transition / Condition / Timeout**.
- **Recovery**: What happens on timeout or fault (e.g. fallback state, retry, abort).
- **Fault codes**: Names or IDs for diagnostics and logs; reference where they’re defined (e.g. ROS 2 msgs).

---

## 5. Cross-link related docs

- Add a **Related docs** section with links to perception, power, safety, compute, etc., so the reader can follow the thread.

---

## 6. Data and protocols

- **CRC / retries**: How errors are detected and handled.
- **Bandwidth budget**: If shared bus or limited throughput, state approximate allocation (e.g. % or kbps per use case).

---

## 7. Tests and acceptance

- Group tests by category: **Environmental**, **Endurance**, **Functional**, **Acceptance** (or similar).
- Tie acceptance to requirements (e.g. “retention force test” vs “≥ 3× mass”).

---

## 8. Track decisions and gaps

- **Risks**: Short list with mitigations.
- **Open questions**: So they don’t get lost (e.g. “PHY choice”, “plating”).
- **Changelog**: Version and date when you add sections or change numbers; keeps history visible.

---

## 9. Keep subsystems index in sync

- When a spec fills a gap listed under **Missing** in [subsystems/INDEX.md](subsystems/INDEX.md), move that item to **Have** and adjust **Next** in the relevant subsystem file (e.g. [subsystems/docking.md](subsystems/docking.md)).

---

## Template snippet

You can start a new spec with something like:

```markdown
# <Title> Spec

↑ [Docs index](../README.md)

<One-line purpose.>

## Scope
- **In scope**: …
- **Out of scope**: … (link to other specs)

## Requirements
| Requirement | Target |

## <Main sections: Mechanical / Electrical / Data / Algorithm / …>

## Thresholds and timeouts
(if applicable)

## Related docs
- [Other spec](path)

## Open questions
- …

## Changelog
| Version | Date | Change |
```

Then expand each section with tables and concrete numbers where it helps.
