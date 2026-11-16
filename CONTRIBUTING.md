# Contributing

Contributions from humans and AI agents are welcome as reviewable proposals.
The repository is in its foundation phase; interfaces are expected to change.

## Before proposing work

1. Follow the README cold-start path.
2. State whether the contribution changes the MRM, CP, renderer, evaluator,
   knowledge record, documentation, or more than one boundary.
3. Label claims `E`, `W`, `H`, or `?` and include conditions and evidence.
4. Separate observed results from interpretation and planned work.
5. For protocol/renderer changes, describe an independent evaluation.
6. For evaluator changes, compare them with the prior method separately from
   any candidate scored by the new method.

## Minimal proposal record

Include:

- a stable proposal title/ID;
- motivation and scope;
- affected versions/files;
- compatibility and migration implications;
- reproducible examples or fixtures where applicable;
- evaluation plan and success/failure thresholds;
- security, privacy, licensing, and provenance notes; and
- explicit limitations and unresolved questions.

Machine-generated contributions MUST identify the generating system when known,
the human submitter/reviewer, supplied context, and material external sources.
Do not claim independent validation merely because a second prompt or run agreed.

## Repository conventions

- Markdown uses one sentence per line when practical and relative links for
  repository documents.
- JSON uses UTF-8, two-space indentation, a final newline, stable IDs, and JSON
  Schema Draft 2020-12.
- Versions are explicit in public identifiers and filenames.
- Generated artifacts are not committed unless a transmission manifest records
  their source, configuration, hash, and status.
- Ground truth intended for blind evaluation stays outside the public tree until
  evaluation is complete.
- Credentials, personal data, model secrets, and unreviewed executable payloads
  are prohibited.
- A change should be small enough to review and should not mix evaluator changes
  with a candidate's claimed improvement.

## Change workflow

Use a short-lived branch and pull request for substantive changes after the
initial repository seed. The pull request should describe evidence actually
produced, checks actually run, and work intentionally deferred. Review does not
promote an epistemic state automatically.

## Licensing note

No repository license has yet been selected. Do not submit third-party content
whose reuse rights are unclear. A contribution process and license must be
adopted before accepting external contributions that require redistribution
rights.
