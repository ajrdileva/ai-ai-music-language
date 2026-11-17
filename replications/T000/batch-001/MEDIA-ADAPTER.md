# Receiver Media Adapter 000

**ID:** `RMA-000`

**Status:** Frozen execution interface; not a communication candidate or evaluator

RMA-000 lets local image-capable receivers inspect the frozen MP4 and WAV
without adding musical interpretation.
It is analogous to a service's private media decoder and is not supplied to
native-multimodal cloud receivers.

The adapter:

- verifies the canonical MP4 and WAV SHA-256 hashes;
- extracts video frames uniformly at exactly 2 frames per second;
- renders one full-duration stereo waveform image;
- renders one full-duration logarithmic-frequency spectrogram image;
- preserves the raw MP4, WAV, and all other package files in the isolated
  receiver workspace; and
- records commands, tool version, parameters, timestamps, file sizes, and
  hashes in `adapter-manifest.json`.

It performs no OCR, transcription, pitch detection, beat detection, event
segmentation, note naming, velocity estimation, or response construction.
Derived images are interface views, not additions to CP-000 and not evidence
that T000 communicates successfully.

Run it with [`prepare_receiver_media.py`](../../../tools/prepare_receiver_media.py).
The expected T000 output is 22 uniformly sampled video frames, one waveform,
one spectrogram, and one manifest.

Every local slot must receive the identical adapter output generated once and
copied byte-for-byte.
Regenerating views with a different adapter or parameter set is a deviation.
