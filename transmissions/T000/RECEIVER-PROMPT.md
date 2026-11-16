# T000 Receiver Prompt v0.1

You are the receiving agent in a blind musical communication experiment.

Using only the supplied T000 receiver package and the public entry points it
declares, recover the transmitted independent note events. Do not seek or use
withheld ground truth, private files, this project's earlier conversations, or
another receiver's answer.

Return exactly one JSON object conforming to
`receiver-response-000.schema.json`. Include:

- the recovered protocol ID and version;
- one reconstructed event per note you believe was transmitted;
- MIDI pitch, onset tick, duration tick, velocity, and confidence per event;
- every artifact, document, prompt, or external source consulted; and
- explicit uncertainty or modality limitations.

Do not add prose outside the JSON object. Event IDs may be receiver-assigned.
Use `480` ticks per quarter note as declared by the protocol package. Acknowledge
failure rather than inventing an event you cannot support.
