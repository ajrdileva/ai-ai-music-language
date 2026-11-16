# Transmission 000 — Baseline Reconstruction

**Status:** Communication baseline evaluated — Run 001 passed

**Artifacts:** Published with frozen hashes

**Independent tests:** One cold-start receiver run complete

**Knowledge evaluation:** Not run; out of scope for this baseline

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
will establish a baseline that later protocols can challenge; it is not intended
to demonstrate an optimal or novel musical language.

## Planned reference material

The MRM fixture will contain:

- individually sounding notes;
- simultaneous/overlapping independent notes;
- different durations and velocities; and
- explicit temporal gaps (silence).

The exact public musical material and any withheld evaluation ground truth will
be fixed with the evaluation plan before the first independent run.

## Planned outputs

- MRM-000 reference instance;
- CP-000 protocol description and cold-start entry point;
- synchronized audio and functional visual representation;
- 16:9 video and generated thumbnail;
- transmission manifest with content hashes;
- reproducibility and validation report;
- receiver response(s); and
- independent IES-C000 communication report.

## Planned communication questions

Can an unfamiliar capable agent, without unpublished conversational context:

1. identify the protocol and find its decoding information;
2. recover pitch, onset, duration, and simultaneity;
3. distinguish silence from missing data;
4. return the required machine-readable response; and
5. state uncertainty and failure accurately?

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
