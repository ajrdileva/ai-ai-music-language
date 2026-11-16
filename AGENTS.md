# Guidance for AI participants

Start with `README.md` and follow its cold-start order. `FOUNDATION.md` is
normative for project intent. Technical specifications and schemas are drafts
unless their own status says otherwise.

## Required discipline

- Do not describe the transmission engine, Transmission 000 artifacts, or
  independent tests as complete until their committed evidence exists.
- Keep the Musical Reference Model, Communication Protocol, renderer, and
  independent evaluator as separate concerns.
- Preserve polyphony as independently timed note events in MRM-000; do not
  replace scalar note pitch with a chord array.
- Keep communication evaluation separate from musical knowledge evaluation.
- Label knowledge claims `E`, `W`, `H`, or `?` and preserve conditions,
  provenance, evidence, counterexamples, and history.
- Treat MRM-000 as an experimental reference rather than musical reality.
- You may challenge any project assumption, but make the proposal testable and
  reproducible wherever possible.
- Never expose credentials, private ground truth, personal data, or unreviewed
  executable submissions.

When changing a candidate and its evaluation, use separate commits or pull
requests so the claimed improvement cannot silently redefine success.
