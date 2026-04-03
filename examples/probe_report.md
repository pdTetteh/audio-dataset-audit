# AudioDatasetAudit Report

## missingness
- Status: **pass**
- Summary: Calculated missing value counts and rates for all columns.
- Metrics:
  - rows: 5
  - missing_counts: {item_id=0, path=0, split=0, label=0, speaker_id=0, device_id=0, date=0, location=0, duration=0}
  - missing_rates: {item_id=0.0, path=0.0, split=0.0, label=0.0, speaker_id=0.0, device_id=0.0, date=0.0, location=0.0, duration=0.0}

## imbalance
- Status: **pass**
- Summary: Computed class distribution from the label column.
- Metrics:
  - class_counts: {clean=2, short=1, broken=1, missing=1}
  - max_to_min_ratio: 2.0
  - num_classes: 4

## duplicates
- Status: **pass**
- Summary: Checked for duplicate item IDs and duplicate file paths.
- Metrics:
  - duplicate_item_id_count: 0
  - duplicate_path_count: 0
- Details:
  - {duplicate_item_ids=[], duplicate_paths=[]}

## split_integrity
- Status: **pass**
- Summary: Checked split labels and summarized split distribution.
- Metrics:
  - split_counts: {train=2, test=2, val=1}
  - invalid_split_values: []
  - missing_core_splits: []

## speaker_id_leakage
- Status: **pass**
- Summary: No cross-split leakage detected for speaker values among 5 unique entries.
- Metrics:
  - field: speaker_id
  - rows_with_field: 5
  - unique_values: 5
  - overlap_count: 0

## device_id_leakage
- Status: **pass**
- Summary: No cross-split leakage detected for device values among 5 unique entries.
- Metrics:
  - field: device_id
  - rows_with_field: 5
  - unique_values: 5
  - overlap_count: 0

## date_leakage
- Status: **pass**
- Summary: No cross-split leakage detected for recording date values among 5 unique entries.
- Metrics:
  - field: date
  - rows_with_field: 5
  - unique_values: 5
  - overlap_count: 0

## location_leakage
- Status: **fail**
- Summary: Detected 1 location value(s) present in more than one split.
- Metrics:
  - field: location
  - rows_with_field: 5
  - unique_values: 3
  - overlap_count: 1
- Details:
  - {value=accra, splits=['train', 'val'], num_splits=2}

## file_existence
- Status: **fail**
- Summary: Detected 1 manifest row(s) pointing to missing files.
- Metrics:
  - rows_checked: 5
  - unique_paths_checked: 5
  - missing_file_count: 1
- Details:
  - {item_id=p005, path=audio/missing.wav, resolved_path=/mnt/data/workrepo/audio-dataset-audit/examples/audio/missing.wav}

## audio_readability
- Status: **fail**
- Summary: Detected 1 existing file(s) that could not be read as audio.
- Metrics:
  - rows_checked: 5
  - unique_paths_checked: 5
  - unreadable_file_count: 1
- Details:
  - {item_id=p004, path=audio/broken.wav, resolved_path=/mnt/data/workrepo/audio-dataset-audit/examples/audio/broken.wav, error=Error opening '/mnt/data/workrepo/audio-dataset-audit/examples/audio/broken.wav': Format not recognised.}

## sample_rate_consistency
- Status: **warn**
- Summary: Observed 2 sample rates; dominant rate is 16000 Hz.
- Metrics:
  - readable_file_count: 3
  - dominant_sample_rate: 16000
  - dominant_count: 2
  - sample_rate_counts: {8000=1, 16000=2}
  - mismatch_count: 1
- Details:
  - {item_id=p002, path=audio/stereo_8k.wav, sample_rate=8000, dominant_sample_rate=16000}

## channel_consistency
- Status: **warn**
- Summary: Observed 2 channel layouts; dominant layout uses 1 channel(s).
- Metrics:
  - readable_file_count: 3
  - dominant_channels: 1
  - dominant_count: 2
  - channel_count_distribution: {1=2, 2=1}
  - mismatch_count: 1
- Details:
  - {item_id=p002, path=audio/stereo_8k.wav, channels=2, dominant_channels=1}

## duration_sanity
- Status: **warn**
- Summary: Duration analysis flagged zero-length, extreme, or manifest-mismatched files.
- Metrics:
  - readable_file_count: 3
  - min_duration: 0.02
  - median_duration: 1.0
  - max_duration: 1.0
  - zero_duration_count: 0
  - suspicious_short_count: 1
  - suspicious_long_count: 0
  - manifest_duration_mismatch_count: 1
  - manifest_has_duration: True
- Details:
  - {item_id=p003, path=audio/short_16k.wav, issue=very_short, duration=0.02}
  - {item_id=p003, path=audio/short_16k.wav, issue=manifest_duration_mismatch, manifest_duration=0.5, probed_duration=0.02, delta=0.48}
