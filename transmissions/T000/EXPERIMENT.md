# T000 Experiment Design v0.1

**Status:** Preregistered design draft; no receiver run completed  
**Question:** Can an unfamiliar capable AI recover the independent MRM-000 note
events using only the published cold-start package?

## Candidate

T000 uses the fixed idea **Three Tones, Four Temporal States**. The fixture has
twelve note events across four temporal phases:

1. three separate note events;
2. three simultaneous onsets with independent durations;
3. three staggered onsets with a common ending; and
4. three separate events in reverse pitch order.

The fixture includes silence and three velocities. Exact pitches, timing, event
IDs, and the canonical MRM file remain withheld until the blind run is closed.
The public commitment procedure will bind the fixture before a receiver is
tested.

## Receiver package

The receiver may receive only:

- the canonical T000 video and/or explicitly declared artifacts;
- its manifest and hashes;
- `protocols/cp-000-baseline.json` and its linked public documents/schemas; and
- a neutral prompt requesting a `RECEIVER-RESPONSE-000` object.

The receiver must not receive this conversation, the private fixture, renderer
debug data, a MIDI file, or prior receiver answers. Every consulted item must be
listed in `context_used`.

## Primary response

The response must validate against
[`receiver-response-000.schema.json`](../../schemas/receiver-response-000.schema.json).
Raw output is preserved before normalization or scoring.

## Preregistered matching and metrics

Events are matched one-to-one. A candidate match requires exact pitch and an
onset within 60 ticks. Among candidates, the scorer minimizes onset error, then
duration error, without reusing an event.

Primary metrics:

- event precision, recall, and F1;
- exact pitch accuracy among matched events;
- onset mean absolute error and proportion within 60 ticks;
- duration mean absolute error and proportion within 60 ticks;
- exact recovery of simultaneous-onset and common-ending relationships;
- protocol ID/version recovery without extra context; and
- extra, omitted, duplicated, or invalid events.

Velocity mean absolute error and proportion within 8 MIDI velocity units are
secondary metrics for v0.1 because brightness/audio amplitude perception may
vary by receiver modality.

## Confirmatory success threshold

The first baseline passes only if one independent cold-start receiver run meets
all of these conditions:

- protocol identity recovered without unpublished context;
- event precision, recall, and F1 equal `1.0`;
- all pitches exact;
- every onset and duration within 60 ticks;
- all simultaneity, overlap, and common-ending relationships recovered; and
- response schema valid with context and uncertainty disclosed.

Velocity results are reported but do not determine the v0.1 verdict. Any metric
or tolerance changed after inspecting a response makes the affected result
exploratory rather than confirmatory.

## Independence and evidence

The receiver does not author the verdict. The evaluator is versioned separately
from the renderer/protocol and preserves the raw response, scoring configuration,
per-event matches, aggregate metrics, environment, and limitations in an
IES-C000 record.

Knowledge development is explicitly out of scope. No result from T000 alone
establishes that an agent understood, discovered, or learned a musical concept.

## Publication sequence

1. Freeze private MRM and publish its salted commitment.
2. Build artifacts and publish their manifest/hashes.
3. Freeze receiver package, prompt, evaluator, and environment declaration.
4. Run the independent receiver and preserve raw output.
5. Score without changing preregistered rules.
6. Publish the revealed fixture/salt, response, IES-C000 report, and limitations.
7. Mark T000 `evaluated` only when those records are publicly linked.
