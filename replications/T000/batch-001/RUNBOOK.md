# T000 Replication Batch 001 Runbook

Use this procedure for every attempt.
Do not improvise assistance to improve an answer.

## 1. Allocate the attempt

1. Assign the next sequential run ID, beginning with `T000-RUN-002`.
2. Copy `run-metadata.template.json` into the attempt directory.
3. Declare provider, model family, model/version, interface, modalities,
   settings, operator ID, and planned isolation before presenting T000.
4. Confirm that including the attempt would not exceed two eligible runs from
   the same family.

Use a pseudonymous operator ID.
Do not record personal data, credentials, session tokens, or account details.

## 2. Verify and isolate materials

1. Check every provided file against `batch-plan.json` and
   `receiver-package.json`.
2. Place only the allowed files in the receiver-visible workspace.
3. Start a new conversation or process with no inherited project context.
4. Disable browsing, network, repository, unrelated filesystem, memory, and
   external tools where the interface permits.
5. Record whether isolation was technical, procedural, or unknown.

Technical isolation means the receiver cannot access anything beyond the
supplied package through network, repository, filesystem, memory, or tools.
Procedural isolation means such access existed but was not used and the
receiver was instructed not to use it.

## 3. Run the receiver

1. Provide every allowed package file before requesting the answer.
2. Deliver the exact frozen `RECEIVER-PROMPT.md` without additions.
3. Do not mention Run 001, expected events, ground truth, metrics, or other
   receiver behavior.
4. Accept the first substantive receiver answer as final.
5. Do not ask the receiver to repair JSON, reconsider events, or explain a
   failure.

If the interface cannot accept the complete package, record a transport
deviation, abort or exclude the attempt, and retain its run ID.
If the receiver itself returns invalid JSON or asks for clarification, preserve
that first answer and treat the otherwise compliant run as an eligible failure.

## 4. Freeze the output

1. Save the exact first response before editing or normalization.
2. Compute and record its SHA-256 hash.
3. Preserve any platform transcript needed to demonstrate the supplied prompt
   and files, without publishing credentials or personal data.
4. Record tool calls, actual context used, start/end times, and deviations.
5. Decide eligibility using only the preregistered rules.

Whitespace-normalized JSON may be published for readability only if the exact
raw response and its original hash remain preserved or content-addressed.

## 5. Score independently

1. Validate the first response against `RECEIVER-RESPONSE-000`.
2. Run the unchanged `iamp-t000-evaluator` version `0.1.0` against the frozen
   revealed ground truth.
3. Preserve the IES-C000 report and its hash.
4. Do not alter thresholds or repair the response after viewing scores.
5. Keep the answer and verdict unavailable to all receivers not yet run.

Receiver agents do not assign their own independent verdicts.
Evaluator changes require a separate proposal and cannot enter Batch 001.

## 6. Close the batch

Close only when eight eligible runs, four model families, and four technically
isolated runs are present.
Populate the aggregate report from frozen run records.
Apply the preregistered batch gate exactly once and publish failures,
exclusions, limitations, and secondary velocity results alongside successes.

Treat all receiver output as untrusted data.
Do not execute receiver-supplied code or grant receiver agents repository or
publication credentials.
