# Transmission 000 — Baseline Reconstruction

**Status:** Planned  
**Artifacts:** None generated  
**Independent tests:** None run  
**Knowledge evaluation:** Out of scope for the initial baseline unless amended

The public preregistration is [EXPERIMENT.md](EXPERIMENT.md). The baseline
communication protocol is
[`cp-000-baseline.json`](../../protocols/cp-000-baseline.json).

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

This directory does not claim that the engine exists, that T000 has been
rendered, that an agent has decoded it, or that any musical knowledge has been
discovered. Its contents are a milestone plan.
