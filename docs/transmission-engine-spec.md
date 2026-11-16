# Transmission Engine Specification v0.1

**Status:** Draft; not implemented  
**Target milestone:** Transmission 000  
**Foundation:** [Project Foundation v0.2](../FOUNDATION.md)

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY**
describe requirements for a future conforming implementation. Their presence
does not imply that an implementation currently exists.

## 1. Scope

This specification defines the minimum interfaces needed to create and evaluate
a reproducible musical transmission:

- MRM-000, the first Musical Reference Model;
- CP-000, a communication-protocol description;
- a renderer contract;
- a transmission manifest;
- independent communication and knowledge evaluation records; and
- epistemic claim records.

It does not define a final AI musical language, a universal ontology of music,
or a completed Transmission 000.

## 2. Versioning and identity

Instances MUST declare a schema/protocol identifier and version. Transmission,
event, group, artifact, claim, evaluation, and protocol IDs MUST be stable within
their declared scope. Breaking semantic changes require a new schema/protocol
version; documentation-only clarifications MAY retain the version with a
revision record.

## 3. MRM-000

### 3.1 Time

MRM-000 uses integer ticks and declares `ticks_per_quarter`. Tempo changes are
ordered events mapping ticks to microseconds per quarter note. A consumer MUST
NOT infer a default tempo when none is declared by the instance or containing
manifest.

### 3.2 Notes and polyphony

Each note event MUST contain:

- a persistent event ID;
- one scalar MIDI pitch (`0..127`);
- non-negative onset tick;
- positive duration tick; and
- MIDI velocity (`0..127`).

Notes MAY overlap freely. Simultaneous notes are independent events with equal
onsets, not one event with a pitch array. Their durations and velocities MAY
differ. Silence is represented by gaps without active notes.

### 3.3 Groups and semantics

Optional groups contain persistent references to one or more events. They MUST
NOT require common onset/duration and MUST NOT imply a chord, phrase, voice, or
other interpretation unless a separately typed semantic assertion says so.

### 3.4 Source fidelity

Normalization MUST record source identity and transformations. Any lossy
conversion MUST document the lost information. Alternative musical models MAY
replace or accompany MRM-000 if their relationship to the baseline is explicit.

## 4. CP-000

A CP-000 description MUST declare:

- protocol ID, version, maturity, and target model/ontology;
- message units, framing, ordering, and termination;
- symbol-to-semantics mappings or a resolvable specification;
- media/channel requirements and synchronization behavior;
- machine-readable bootstrap and human-notice separation;
- decoder entry points and expected response shape;
- integrity and dependency information; and
- known ambiguities, losses, and unsupported features.

The bootstrap MUST be sufficient to locate the protocol definition without an
unpublished conversation. Whether unfamiliar agents can actually recover it is
an evaluation question.

A candidate CP MUST NOT modify ground truth or its evaluator. If a CP proposes
new evaluation criteria, that proposal is reviewed and versioned separately.

## 5. Renderer contract

### 5.1 Inputs

A render job consumes immutable or content-addressed:

1. reference data (MRM-000 or declared alternative);
2. a CP description;
3. render configuration;
4. engine/dependency versions; and
5. media resources such as sound sets and fonts.

### 5.2 Outputs

For Transmission 000 the renderer is expected to produce:

- synchronized audio;
- a cumulative or otherwise decodable visual track;
- regular 16:9 video;
- a generated thumbnail;
- a semantic transmission manifest; and
- a reproducibility/validation report.

Every produced file MUST have media type, byte count, and cryptographic hash in
the manifest. Missing optional output MUST be explicit rather than silently
omitted.

### 5.3 Determinism

The engine SHOULD support deterministic ordering and seeded stochastic steps.
The report MUST declare whether outputs are byte-reproducible, perceptually
reproducible, or not yet reproducible, and why.

### 5.4 Synchronization

Audio, visuals, and protocol frames MUST share a declared timeline. The renderer
MUST report any rounding or resampling between musical ticks, audio samples, and
video frames.

## 6. Transmission manifest

The manifest connects transmission identity, maturity, reference/protocol
versions, input/output hashes, challenge instructions, public entry points, and
evaluation records. A manifest MUST distinguish:

- `planned`: declared but not generated;
- `generated`: artifacts exist but have not completed validation;
- `validated`: internal checks passed under named conditions; and
- `evaluated`: an identified independent evaluation record exists.

These states do not substitute for epistemic claim states.

## 7. Independent evaluation

### 7.1 General rules

The evaluator and fixtures MUST be versioned independently from the candidate.
Metrics, tolerances, allowed context, receiver model/configuration, runs, and
ground-truth handling MUST be fixed before scoring or explicitly labeled
exploratory. Candidate authors MUST NOT assign their own independent verdict.

### 7.2 Communication track (IES-C000)

The communication report SHOULD include, when applicable:

- note-event precision, recall, and F1;
- pitch accuracy;
- onset absolute error in ticks/milliseconds and tolerance hit rate;
- duration absolute/relative error and tolerance hit rate;
- velocity error if velocity is in scope;
- recovery of simultaneous and overlapping events;
- protocol identification/bootstrap success; and
- invalid, omitted, duplicated, or extra events.

A report MUST preserve raw receiver output or a content-addressed reference to
it, scoring configuration, evaluator version, and per-run results.

### 7.3 Knowledge track (IES-K000)

Knowledge evaluation is separate and task-specific. A report SHOULD test one or
more of:

- identification/explanation of a musical relationship;
- application to held-out material;
- transfer to another unfamiliar agent;
- survival under counterexamples or boundary cases;
- comparison against prior knowledge/baselines; and
- accurate uncertainty, provenance, and epistemic status.

Exact rubrics and success thresholds MUST be declared before a confirmatory
evaluation. A communication score MUST NOT be used as a proxy for knowledge.

## 8. Epistemic claim records

Claims use `E`, `W`, `H`, or `?` as defined by Foundation v0.2. Each record MUST
include its claim, conditions/scope, current state, provenance, and state
history. `E` requires a cited evaluation under named conditions. `W` and `H`
MUST describe supporting evidence and missing validation. `?` SHOULD be framed
as a resolvable question where possible.

Promotion, demotion, challenge, refinement, and supersession append new history.
They do not erase prior evidence or counterexamples.

## 9. Cold-start conformance

A published transmission MUST provide a stable, public entry point containing or
linking to protocol identity, machine-readable schema, decoding instructions,
challenge response shape, and integrity data. A cold-start test MUST record what
the receiver was given and MUST NOT silently add conversational context.

## 10. Transmission 000 acceptance gates

T000 is complete only when all of the following evidence exists:

1. A valid MRM instance exercising single notes, polyphony, unequal durations,
   and silence.
2. A valid CP instance and cold-start decoder path.
3. Rebuildable renderer source/configuration and hashed artifacts.
4. A manifest and reproducibility report.
5. A preregistered communication evaluation configuration.
6. At least one independent receiver run and IES-C000 report.
7. Accurate documentation of failures, uncertainty, and limitations.

Knowledge evaluation MAY be out of scope for T000, but that decision MUST be
explicit. Until these gates are met, repository references to T000 remain
`planned` or the most accurate intermediate status.

## 11. Draft schemas

- [`mrm-000.schema.json`](../schemas/mrm-000.schema.json)
- [`cp-000.schema.json`](../schemas/cp-000.schema.json)
- [`transmission-manifest-000.schema.json`](../schemas/transmission-manifest-000.schema.json)
- [`ies-c000.schema.json`](../schemas/ies-c000.schema.json)
- [`ies-k000.schema.json`](../schemas/ies-k000.schema.json)
- [`knowledge-claim-000.schema.json`](../schemas/knowledge-claim-000.schema.json)

Schema validity alone is not experimental validity.
