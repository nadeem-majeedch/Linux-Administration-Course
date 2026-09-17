# Lecture Slides — Index & Conventions

> Eight unit-level decks cover the curriculum. The 30-module content is
> delivered **through** these decks — each slide cites its module source
> so depth always lives in the modules, never in the deck.

## Deck index

| Deck | Unit / Modules | Sessions | Delivery time | Prerequisites | Associated lab | Assessment link |
|---|---|---|---|---|---|---|
| [Unit 1 — Foundations](unit-01-foundations-slides.md) | M01–M04 | S1–S4 | 4 × 60' lecture (rest hands-on) | none | M04 install + snapshots | M01–M04 quizzes |
| [Unit 2 — Command Line Fluency](unit-02-command-line-slides.md) | M05–M09 | S5–S8 | 4 × 55' lecture | working VM | M05–M09 labs | M05–M09 quizzes; LA-1 |
| [Unit 3 — Scripting & Automation](unit-03-scripting-automation-slides.md) | M10–M11 | S9–S10 | 2 × 55' lecture | Unit 2 fluency | M10 labs + Mini-Project A | M10–M11 quizzes; A1 |
| [Unit 4 — System Administration](unit-04-system-administration-slides.md) | M12–M15 | S11–S12 | 2 × 55' lecture | Unit 2 | M12/M14 labs + Mini-Project B | M12–M15 quizzes; LA-3; **midterm scope ends here** |
| [Unit 5 — Software, Storage & Time](unit-05-software-storage-time-slides.md) | M16–M19 | S15–S18 | 4 × 50' lecture | snapshotted VM | M16–M19 labs | M16–M19 quizzes; LA-2 |
| [Unit 6 — Services, Network & Security](unit-06-services-network-security-slides.md) | M20–M25 | S19–S24 | 6 × 50' lecture | Units 1–5 | M20–M25 labs | M20–M25 quizzes; LA-4 |
| [Unit 7 — The Data Science Stack](unit-07-data-science-stack-slides.md) | M26–M29 | S25–S28 | 4 × 50' lecture | Unit 6 | M26–M29 labs + Mini-Project D | M26–M29 quizzes |
| [Unit 8 — Capstone](unit-08-capstone-slides.md) | M30–M32 | S29–S30 | 2 × 50' lecture | all | M31 DS-server lab, M32 drills | capstone rubric; practical + final |

## How a deck is built (conventions)

Every slide has four parts:

```markdown
# Slide N — Title
## Slide Content            ← what students see
## Instructor Delivery Notes ← how to teach it, what to emphasize
## Visual or Demonstration Suggestion
## Student Question
```

- Decks are **teaching instruments, not content duplicates** — each
  deck section names its module; the module lesson is the reading and
  the lab is the practice.
- Knowledge-check slides appear every 3–4 slides; every deck ends with
  a summary, exit ticket, and homework pointing at the module quizzes.
- All commands/outputs shown are drawn from the module pages (validated)
  or marked as variable.

## Module → deck-section fast map

| Module | Deck § | Module | Deck § |
|---|---|---|---|
| M01 | U1 §1–2 | M16 | U5 §1 |
| M02 | U1 §3 | M17 | U5 §2 |
| M03 | U1 §4 | M18 | U5 §3 |
| M04 | U1 §5–6 | M19 | U5 §4 |
| M05 | U2 §1 | M20 | U6 §1 |
| M06 | U2 §2 | M21 | U6 §2 |
| M07 | U2 §3 | M22 | U6 §3 |
| M08 | U2 §4 | M23 | U6 §4 |
| M09 | U2 §5 | M24 | U6 §5 |
| M10 | U3 §1–2 | M25 | U6 §6 |
| M11 | U3 §3 | M26 | U7 §1 |
| M12 | U4 §1 | M27 | U7 §2 |
| M13 | U4 §1b | M28 | U7 §3 |
| M14 | U4 §2 | M29 | U7 §4 |
| M15 | U4 §3 | M30–M32 | U8 |

## Using decks without a projector

Each deck is plain Markdown: it prints cleanly, converts to
`marp`/PowerPoint trivially, or can be shared as-is for flipped
classrooms (then the Student Question sections become the classroom
agenda).
