# T000 Multi-Agent Replication — Batch 001

**Status:** Preregistered; no new receiver runs have begun

**Track:** Communication replication (IES-C000)

**Candidate:** Frozen T000 / CP-000 baseline

**Knowledge evaluation:** Not performed

This batch asks whether the T000 cold-start result generalizes beyond the single
receiver reported in Run 001.
It does not modify the transmission, receiver prompt, response schema,
evaluator, or per-run acceptance gate.

## Start here

1. Read the human-readable [preregistration](PREREGISTRATION.md).
2. Inspect the machine-readable [batch plan](batch-plan.json).
3. Inspect the locked [receiver roster](ROSTER.md) and its
   [machine-readable allocation](roster.json).
4. Complete the [transport preflight](PREFLIGHT.md) without presenting T000.
5. Follow the [runbook](RUNBOOK.md) without improvising receiver assistance.
6. Copy [run-metadata.template.json](run-metadata.template.json) for every
   attempt, including excluded and aborted attempts.
7. Populate [aggregate-report.template.json](aggregate-report.template.json)
   only after run records have been frozen.

The machine-readable batch plan controls numeric thresholds, exact hashes, and
eligibility requirements.
The prose documents explain that plan and may not silently override it.

## Planned scope

- eight eligible new runs;
- at least four declared model families;
- no more than two eligible runs from one family;
- at least four runs with technical context isolation;
- identical receiver materials and exact neutral prompt;
- unchanged deterministic evaluator; and
- Run 001 treated only as prior evidence, not as a batch member.

The locked no-cost roster allocates two slots each to OpenAI-GPT, Gemini,
Qwen2.5-VL, and Llama-3.2-Vision.
Six slots are planned with technical isolation; the two personal ChatGPT slots
are procedural.

The first planned attempt is `T000-RUN-002`.
No aggregate or cross-agent generalization claim exists until the batch closes.
