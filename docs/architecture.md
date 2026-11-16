# Architecture

**Status:** Draft design documentation  
**Applies to:** Proposed Transmission Engine v0.1

## Design objective

The architecture minimizes assumptions shared by every experiment. It provides a
stable baseline without treating MIDI, note events, a renderer, or today's
metrics as final definitions of music or intelligence.

## Components and ownership

| Component | Owns | Must not own |
| --- | --- | --- |
| Musical Reference Model (MRM) | Reference events, timing, stable IDs, source provenance | Protocol symbols, visual style, success criteria |
| Communication Protocol (CP) | Encoding, framing, bootstrap, symbol semantics | Ground-truth mutation, evaluation verdicts |
| Renderer | Deterministic audiovisual/materialized artifacts | Musical truth, protocol success |
| Manifest | Version/provenance links and artifact hashes | Undeclared interpretation |
| Independent evaluator | Pre-registered fixtures, metrics, results | Candidate protocol/renderer implementation |
| Knowledge record | Claims, evidence, epistemic history, relations | Automatic promotion of claims |

## Reference data flow

```text
MIDI / structured events / alternative source
                    │
                    ▼
           normalize + validate
                    │
                    ▼
             MRM instance ───────────────┐
                    │                    │ ground truth (withheld when blind)
                    ▼                    │
              CP encoder                │
                    │                    │
                    ▼                    │
          renderer + artifact writer    │
                    │                    │
                    ▼                    │
 audio / visual / video / manifest      │
                    │                    │
                    ▼                    │
           independent receiver         │
                    │                    │
                    ▼                    │
       reconstruction and/or claims ────┘
                    │
                    ▼
    independent communication and knowledge evaluation
```

## MRM-000: note-event reference model

MRM-000 represents a note as one event with a scalar MIDI pitch, onset tick,
duration tick, velocity, and persistent ID. Polyphony is created by overlapping
events. This preserves independent durations and velocities within simultaneous
material.

Silence is represented by an interval without sounding note events. Optional
groups reference event IDs and may suggest structural relationships, but a group
does not by itself assert a chord, voice, phrase, or theory. Semantic
interpretations belong in declared objects or knowledge claims.

An alternative ontology may coexist with MRM-000. It must declare whether it:

- losslessly maps to MRM-000;
- maps partially and documents loss;
- uses MRM-000 only as an evaluation projection; or
- rejects the projection and proposes an independent experimental comparison.

## CP-000: communication protocol description

CP-000 is a protocol *description*, not the final musical language. It identifies
the protocol/version, declares media and framing, defines symbols and semantics,
publishes cold-start entry points, and specifies integrity/reproducibility data.

A CP may encode an MRM or a different declared ontology. It cannot silently
change the MRM ground truth or its own evaluation criteria.

## Renderer boundary

The renderer consumes validated reference data, a protocol description, and a
render configuration. It produces artifacts plus hashes and a report. Given the
same declared inputs, engine version, dependencies, fonts/sound resources, and
configuration, a renderer should be reproducible to the level declared in its
report. Byte-identical output is preferred but must not be claimed when platform
codecs or synthesis prevent it.

Renderer output may include synchronized audio, visuals, a 16:9 video, a
thumbnail, a semantic manifest, and validation metadata. A renderer may expose a
protocol defect; it may not decide that a receiver understood the protocol.

## Independent evaluation

The evaluator is versioned separately and reads immutable candidate artifacts,
pre-registered ground truth or fixtures, and receiver responses. A protocol or
renderer proposal may recommend metrics, but adoption/change of evaluator rules
requires a separate review, rationale, and comparison with the prior method.

Two reports remain independent:

1. **Communication:** event/protocol recovery, including pitch, onset, duration,
   velocity where tested, overlap/simultaneity, and cold-start behavior.
2. **Knowledge:** concept identification, generalization to unseen material,
   successful teaching/transfer, counterexample robustness, and epistemic
   discipline.

Passing communication does not imply musical understanding. Passing a knowledge
task does not excuse failure to report communication results accurately.

## Provenance and epistemic history

Every authoritative artifact and claim uses a stable ID and version. Content
hashes should identify immutable files. Claims retain authorship/agent identity
as declared, evidence, conditions, dependencies, counterexamples, and status
history. Status changes append history rather than rewriting the earlier state.

## Security and blind evaluation

- Credentials, private keys, and publication tokens never enter transmissions.
- Untrusted contributions are data until reviewed; they do not execute by
  default.
- Withheld ground truth stays outside public version control until the blind
  evaluation ends.
- Publication remains human-controlled until a separate security model exists.
- External content is pinned or hashed when reproducibility depends on it.

## Proposed package boundaries

Implementation is intentionally deferred. A future engine may use these logical
boundaries without being required to use these exact package names:

```text
engine/reference/     parsing, normalization, MRM validation
engine/protocol/      CP loading and encoding
engine/render/        audio, visuals, video, thumbnail
engine/manifest/      provenance, hashes, artifact inventory
evaluation/           independently versioned evaluators and fixtures
```
