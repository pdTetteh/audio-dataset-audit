## Goal
Extend AudioDatasetAudit beyond metadata auditing by probing audio files directly.

## Checks to add
- file existence
- audio readability
- sample-rate consistency
- channel-count consistency
- duration sanity checks
- manifest-vs-probed duration mismatch

## Why this matters
Many speech/audio datasets contain silent file-level issues that affect training and evaluation:
- missing files
- corrupted files
- inconsistent sample rates
- unexpected stereo/mono mixtures
- zero-length files
- inaccurate duration metadata

## Deliverables
- `audio_probe.py`
- new file-level checks
- tests
- README update
- example report
