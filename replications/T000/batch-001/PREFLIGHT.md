# Batch 001 Transport Preflight

Preflight verifies transport and configuration without presenting T000 to a
model and without requesting a substantive answer.
It is not a receiver attempt.

## Common checks

- Verify every candidate and execution-lock hash in `batch-plan.json`.
- Confirm the slot is unresolved and no prior Batch 001 result is visible.
- Confirm the exact provider, family, model/build, interface, and settings.
- Confirm ground truth, prior answers, live repository access, memory, search,
  connectors, and unrelated tools are unavailable or disabled as declared.
- Confirm the full raw package can enter the receiver boundary.
- Confirm raw-response capture is ready and will refuse overwrite.

Do not upload T000 merely to test an interface.
Use an unrelated disposable media file for format checks.

## ChatGPT slots

- Use the web interface in an **Unpersonalized Temporary Chat**.
- Resolve the primary or declared fallback before uploading any T000 file.
- Disable automatic model switching, search, connectors, and custom
  instructions.
- Confirm the interface accepts JSON, Markdown, PNG, WAV, and MP4 attachments.
- Treat both slots as procedurally isolated.

## Gemini API slots

- Resolve the exact API model identifier before uploading T000.
- Send no system instruction, tools, grounding, URL, repository reference, or
  conversation history.
- Confirm raw binary multimodal parts can be submitted in one request.
- Restrict the receiver process to API transport and the supplied request.

## Local slots

- Verify the exact Ollama model tag and installed manifest digest.
- Generate RMA-000 views once; verify their manifest before either local run.
- Disable network access after model installation.
- Mount only the frozen package, adapter views, response schema, and prompt.
- Send all views and the exact prompt in one request with the locked settings.

If a preflight fails, record the failure without allocating a run ID because no
receiver has seen T000.
If T000 has crossed the receiver boundary, allocate the planned attempt ID and
follow the runbook even when transport later fails.
