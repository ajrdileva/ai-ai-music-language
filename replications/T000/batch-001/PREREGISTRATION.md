# T000 Multi-Agent Replication Preregistration v0.1

**Batch ID:** `T000-REPLICATION-BATCH-001`

**Status:** Frozen before the first new receiver attempt

**Research track:** Communication replication

## Question

Can a diverse batch of unfamiliar AI receiver agents recover the frozen T000
communication target from the identical cold-start package under controlled
context conditions?

## Prior evidence

T000 Receiver Run 001 passed the preregistered per-run communication gate.
That result motivated this replication but is excluded from all Batch 001
counts and thresholds.
The batch begins with cross-agent generalization in epistemic state `?`.

## Frozen candidate and evaluator

The candidate is the exact T000 receiver package, prompt, protocol, artifacts,
and response schema identified by hashes in
[`batch-plan.json`](batch-plan.json).
The evaluator remains `iamp-t000-evaluator` version `0.1.0` with the frozen
source hash in that plan.

No receiver may receive the revealed ground truth, another receiver answer,
this project's prior conversations, repository files outside the allowed
package, or evaluator output from an earlier batch attempt.

Because the T000 ground truth is now public, at least four eligible runs must
use technical isolation that prevents repository, network, or tool access
beyond the supplied package.
Procedurally isolated runs are allowed only when access was available but not
used and is fully disclosed.

## Sampling plan

The confirmatory batch closes with exactly eight eligible new runs.
It must include at least four declared model families, no more than two eligible
runs from any one family, and at least four technically isolated runs.

Model family means the declared product or model lineage, not merely a renamed
interface or a minor version string.
This is a diversity control, not a claim that the families are statistically
independent.

Attempts receive sequential IDs beginning with `T000-RUN-002`.
Excluded and aborted attempts retain their IDs and records and are replaced by
later IDs until the eligible target is met.

### Pre-run execution lock

Before Run 002 and before observing any new result, the project froze
[`roster.json`](roster.json): two slots each for OpenAI-GPT, Gemini,
Qwen2.5-VL, and Llama-3.2-Vision.
The declared primary/fallback selection rule resolves cloud availability only
during transport preflight and cannot respond to experimental outcomes.

Six slots are designated for technical isolation.
Local image-capable receivers use the frozen neutral
[RMA-000 media adapter](MEDIA-ADAPTER.md), which decodes uniform video frames,
a waveform, and a spectrogram without OCR, pitch detection, segmentation, or
musical interpretation.
The roster and adapter are execution controls; they do not change CP-000, the
T000 candidate, the receiver prompt, the evaluator, or any success threshold.

## Identical-context rule

Every receiver receives the exact files marked `provided` in the batch plan and
the unchanged `RECEIVER-PROMPT.md` in a fresh context.
All files must be made available before the receiver answers.
The receiver may choose which supplied files to inspect but must disclose them
in `context_used`.

No follow-up explanation, coaching, JSON repair prompt, or error correction is
allowed after the receiver produces its first substantive answer.
A malformed or incorrect first answer is an eligible failure if the run was
otherwise compliant.

## Per-run confirmatory gate

A run passes only if all original T000 requirements hold:

- the response validates against `RECEIVER-RESPONSE-000`;
- protocol ID and version are recovered without extra context;
- event precision, recall, and F1 equal `1.0`;
- all pitches are exact;
- every matched onset and duration is within 60 ticks;
- simultaneity, overlap, and common-ending relationships are exact;
- context and uncertainty are disclosed; and
- no forbidden context was used.

Velocity MAE and the proportion within eight MIDI velocity units remain
secondary, non-gating metrics.

## Batch confirmatory gate

The batch passes only after all sampling requirements are satisfied and:

- at least six of eight eligible runs pass;
- the eligible-run pass rate is at least `0.75`; and
- at least three distinct model families produce a passing run.

If eight eligible runs exist but any threshold fails, the batch fails.
If the run count, family diversity, or technical-isolation requirement cannot
be met, the result is inconclusive rather than a pass or failure.
No early success or failure declaration is permitted.

## Eligibility and deviations

Exclude and replace attempts affected by transport failure before the receiver
receives the full package, inherited project context, access to ground truth or
prior answers, follow-up coaching, undeclared external context, or an inability
to identify the actual receiver model family.

Do not exclude a run because the receiver misunderstood the protocol, returned
invalid JSON, omitted events, or failed a metric.
Those are experimental failures.

Every attempted run must preserve a metadata record and exclusion or abortion
reason.
Any change to the candidate, evaluator, thresholds, or eligibility rules after
the first new attempt starts creates a separately versioned exploratory batch.
Any roster, model-selection, or media-adapter change after that point also
requires a new version and cannot enter Batch 001.

## Reporting

Freeze the raw first response before validation, normalization, or scoring.
Record its cryptographic hash and exact supplied context.
Publish one run metadata record, raw response, and IES-C000 report per eligible
run.
Do not expose receiver answers or results to remaining agents until the batch
has closed.

The aggregate report must include every attempt, exclusions, family counts,
isolation counts, individual verdicts, pass rate, family-pass count, secondary
velocity metrics, limitations, and an epistemic interpretation.

## Epistemic interpretation

A passing batch supports `W`, not universal `E`, for this bounded claim:

> CP-000 supports reproducible cold-start recovery across the sampled receiver
> families under the preregistered package and context conditions.

The batch cannot establish universal generalization, musical understanding,
knowledge development, successful velocity recovery, statistical independence
of model families, or protection against future training-data contamination.
