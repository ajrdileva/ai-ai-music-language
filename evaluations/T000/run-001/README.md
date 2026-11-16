# T000 Independent Receiver Run 001

**Track:** Communication (IES-C000)

**Verdict:** Pass under the preregistered v0.1 threshold

**Knowledge evaluation:** Not performed

## Result

One independent receiver was started without this project's conversation
history and instructed to use only the frozen receiver package. It returned a
schema-valid response before ground truth was revealed.

The frozen evaluator reported:

| Metric | Result |
| --- | ---: |
| Event precision / recall / F1 | 1.0 / 1.0 / 1.0 |
| Exact pitch accuracy | 1.0 |
| Onset MAE | 0 ticks |
| Duration MAE | 0 ticks |
| Simultaneous-onset relationships | Exact |
| Common-ending relationships | Exact |
| Overlap relationships | Exact |
| Protocol recovery | Successful |
| Forbidden context used | No |
| Velocity MAE (secondary) | 11.0 MIDI units |
| Velocity within ±8 (secondary) | 0.0 |

The confirmatory communication gate passed because velocity was preregistered as
a reported but non-gating secondary metric. Its systematic overestimate is a
real limitation and candidate target for T001.

## Evidence

- [`raw-response.json`](raw-response.json) — receiver content preserved; JSON
  whitespace was normalized for publication.
- [`ies-c000-report.json`](ies-c000-report.json) — frozen evaluator output.
- [`../../../transmissions/T000/receiver-package.json`](../../../transmissions/T000/receiver-package.json) — exact allowed inputs and hashes.
- [`../../../transmissions/T000/reveal/`](../../../transmissions/T000/reveal/) — exact ground truth, salt, and commitment verification.
- [`../../../transmissions/T000/artifacts/`](../../../transmissions/T000/artifacts/) — published candidate artifacts and frozen manifest.

## Epistemic interpretation

**`E` under these conditions:** one independent receiver recovered all 12
reference events' pitches, onsets, durations, and tested temporal relationships
from the frozen CP-000 baseline package.

This status is bounded to Run 001. It is not evidence of musical knowledge,
generalization across agents, protocol efficiency, or successful velocity
recovery.

The receiver shared the execution host with the experiment but received no
inherited conversation and was explicitly prohibited from accessing paths
outside the package. That boundary was procedural rather than an operating-
system sandbox. The receiver disclosed only package files, and the evaluator
found no declared forbidden context; a future replication should enforce the
boundary technically as well as procedurally.
