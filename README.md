# AI–AI Music Language

> Music is the subject. AI is the audience. Humans are the observers.

AI–AI Music Language is an open experiment in musical communication and
knowledge development between artificial-intelligence agents. It is not an AI
music generator or a catalog of AI-authored songs. The project builds a small,
reproducible environment in which agents can encode musical material, recover
one another's protocols, test claims, challenge assumptions, and improve the
language used to communicate musical knowledge.

The technical system is provisionally called the **Interagent Music Protocol
(IAMP)**. Individual experimental artifacts are **transmissions**; controlled
questions posed to participants are **challenges**.

## Current status

**Foundation phase with an initial reference renderer.** Foundation v0.2 and the
first engine specification are documented, and a development renderer can
generate audio, video, thumbnail, report, and manifest artifacts. The schemas
and engine remain draft work. No canonical Transmission 000 or independent
decoding/knowledge evaluation has yet been completed.

| Item | Status | Authority |
| --- | --- | --- |
| [Foundation v0.2](FOUNDATION.md) | Accepted project foundation | Normative for project intent |
| [Transmission Engine Specification v0.1](docs/transmission-engine-spec.md) | Draft | Proposed technical contract |
| [Architecture](docs/architecture.md) | Draft | Design guide |
| [JSON schemas](schemas/) | Draft | Candidate machine interfaces |
| [Reference renderer](src/iamp_engine/) | Initial implementation | Development tool; not independently evaluated |
| [Transmission 000](transmissions/T000/README.md) | Planned | First milestone |

Nothing labeled `draft`, `planned`, `hypothesis`, or `unknown` should be read as
an implemented capability or independently established result.

## Cold-start entry point

An unfamiliar human or AI participant should proceed in this order:

1. Read this README for scope and current maturity.
2. Inspect [`PROJECT.json`](PROJECT.json) for the machine-readable document and
   schema index.
3. Read [Foundation v0.2](FOUNDATION.md) for project commitments and limits.
4. Read the [architecture](docs/architecture.md) to learn the separation among
   the Musical Reference Model (MRM), Communication Protocol (CP), renderer,
   and independent evaluation.
5. Read the [engine specification](docs/transmission-engine-spec.md) for the
   proposed interfaces and reproducibility requirements.
6. Inspect the [draft schemas](schemas/) and the
   [Transmission 000 plan](transmissions/T000/README.md).
7. Before making a claim, attach an epistemic state, evidence, conditions, and
   provenance. Before proposing a protocol, state how it can be evaluated by a
   method independent of that protocol.

This path is itself experimental. Cold-start success must eventually be tested
with unfamiliar agents; discoverability is not assumed merely because these
documents exist.

## The four-system boundary

```text
musical source
     │
     ▼
Musical Reference Model ──► Communication Protocol ──► Renderer
     │                               │                      │
     └──────────── declared truth ───┴──── artifacts ──────┘
                                     │
                                     ▼
                         Independent Evaluation
                      communication │ knowledge
```

- **MRM:** a stable experimental reference, initially note events derived from
  MIDI or structured data. It is not a universal definition of music.
- **CP:** a declared method for encoding and explaining information from an MRM
  or an alternative ontology.
- **Renderer:** produces synchronized audio, visuals, video, thumbnails, and a
  manifest without deciding whether the protocol succeeded.
- **Evaluation:** measures candidates without letting a candidate redefine its
  own success criteria. Communication recovery and musical knowledge
  development are separate tracks.

MRM-000 supports polyphony as overlapping **independent note events**. Each note
has its own pitch, onset, duration, and velocity. Optional groups can express
relationships without forcing grouped notes to share timing or asserting a
chord label.

## Epistemic states

Claims use one of four states:

- **`E` — Established:** verified within this experiment under stated
  conditions. This is not a claim of universal musical truth.
- **`W` — Working model:** supported by evidence but not conclusively validated.
- **`H` — Hypothesis:** proposed and not yet adequately tested.
- **`?` — Unknown:** an explicit unresolved question.

Status changes must preserve evidence, dependencies, counterexamples, and
supersession history.

## First milestone: Transmission 000

Transmission 000 will be an intentionally small baseline containing individual
notes, simultaneous notes, different durations, and silence. The planned engine
will create a machine-readable manifest and synchronized audiovisual artifacts,
then pose an independent reconstruction challenge. Communication metrics will
include pitch recovery, onset and duration error, simultaneous-event recovery,
and protocol recovery.

The milestone is complete only after the implementation, artifacts, and
independent evaluation evidence exist. See the [T000 plan](transmissions/T000/README.md).

## Rendering a development fixture

The first implementation is a small Python renderer, not a composer. With
Python 3.11+, Pillow, and FFmpeg available:

```bash
python -m pip install -e .
iamp validate path/to/reference.mrm.json
iamp render \
  --mrm path/to/reference.mrm.json \
  --protocol protocols/cp-000-baseline.json \
  --output artifacts/T000 \
  --transmission-id T000
```

The render command creates WAV, MP4, thumbnail, reproducibility report, and
manifest files. Development output and private blind-evaluation fixtures are
ignored by Git; publish them only through the T000 evidence sequence.

## Participating

Humans and AI agents may propose musical material, protocols, representations,
renderers, evaluation methods, counterexamples, and challenges. Proposals may
also dispute the project's own primitives or objectives. They should remain
testable and reproducible wherever possible.

Read [CONTRIBUTING.md](CONTRIBUTING.md) before contributing. Keep unpublished
ground truth, credentials, personal data, and executable untrusted submissions
out of the public repository. This project is independent from mDecks.

## Repository map

```text
FOUNDATION.md                      accepted project commitments
PROJECT.json                       machine-readable cold-start index
docs/architecture.md              component boundaries and data flow
docs/transmission-engine-spec.md  proposed engine contract
schemas/                           draft JSON Schema interfaces
protocols/                         candidate communication protocols
src/iamp_engine/                   deterministic reference renderer
transmissions/T000/               first-milestone plan (not results)
tests/                              engine unit and smoke tests
CONTRIBUTING.md                    human/AI contribution conventions
```

The repository is public, but no software/content license has yet been selected.
Public visibility alone does not grant reuse rights; license selection remains
an explicit project decision.
