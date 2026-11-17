# Transmission 000 — Baseline Reconstruction

**Status:** Communication baseline evaluated — Run 001 passed

**Artifacts:** Published with frozen hashes

**Independent tests:** One cold-start receiver run complete

**Knowledge evaluation:** Not run; out of scope for this baseline

**Public distribution:** [YouTube](https://www.youtube.com/watch?v=swVxblM6HjI), with a
separate [publication record](publications/youtube.json)

The public preregistration is [EXPERIMENT.md](EXPERIMENT.md). The baseline
communication protocol is
[`cp-000-baseline.json`](../../protocols/cp-000-baseline.json).
Before the run, the exact fixture was bound by the public
[`ground-truth-commitment.json`](ground-truth-commitment.json); its salt and
contents are now published in [`reveal/`](reveal/) so the commitment can be
verified.
The frozen neutral receiver instructions are
[`RECEIVER-PROMPT.md`](RECEIVER-PROMPT.md).
The exact allowed file inventory and hashes are
[`receiver-package.json`](receiver-package.json).

## Purpose

T000 is the smallest reproducible test of cold-start musical communication. It
establishes a baseline that later protocols can challenge; it is not intended
to demonstrate an optimal or novel musical language.

## Revealed reference material

The revealed [MRM fixture](reveal/ground-truth.mrm.json) contains:

- individually sounding notes;
- simultaneous/overlapping independent notes;
- different durations and velocities; and
- explicit temporal gaps (silence).

The fixture was fixed before the independent run by the published salted
commitment and revealed only after the raw receiver response was frozen.

## Published outputs

- [MRM-000 reference instance](reveal/ground-truth.mrm.json);
- [CP-000 protocol description](../../protocols/cp-000-baseline.json) and
  [cold-start receiver instructions](RECEIVER-PROMPT.md);
- synchronized [audio](artifacts/T000.wav) and functional visual
  [video](artifacts/T000.mp4);
- generated [thumbnail](artifacts/T000-thumbnail.png);
- [transmission manifest](artifacts/manifest.json) with content hashes;
- [reproducibility report](artifacts/reproducibility-report.json);
- frozen [receiver response](../../evaluations/T000/run-001/raw-response.json);
- independent [IES-C000 communication report](../../evaluations/T000/run-001/ies-c000-report.json).

## Evaluated communication questions

Can an unfamiliar capable agent, without unpublished conversational context:

1. identify the protocol and find its decoding information;
2. recover pitch, onset, duration, and simultaneity;
3. distinguish silence from missing data;
4. return the required machine-readable response; and
5. state uncertainty and failure accurately?

Receiver Run 001 passed the preregistered communication threshold under its
recorded conditions.
The exact evidence and limitations are preserved in the
[Run 001 record](../../evaluations/T000/run-001/README.md).

## Public distribution

The canonical T000 video artifact remains
[`artifacts/T000.mp4`](artifacts/T000.mp4), identified by the frozen manifest
hash.
The [YouTube publication](https://www.youtube.com/watch?v=swVxblM6HjI) is a
public distribution copy and cold-start surface.
Its machine-readable [publication record](publications/youtube.json) preserves
the uploaded source hash, platform ID, public-visibility observation, and
viewer-facing checks without modifying the frozen artifact manifest.
No byte identity is claimed for platform playback, and publication adds no new
communication or knowledge-evaluation evidence.

## Acceptance

Acceptance is governed by section 10 of the
[Transmission Engine Specification](../../docs/transmission-engine-spec.md).
No checkbox is marked complete until its evidence is committed or linked by a
content-addressed public record.

## Non-claims

Run 001 establishes only that one independent receiver recovered the baseline
communication target under the recorded conditions. It does not establish that
the protocol generalizes, that other agents will succeed, or that any musical
knowledge was understood, learned, or discovered. Velocity recovery missed the
secondary tolerance and is preserved as an experimental limitation.
