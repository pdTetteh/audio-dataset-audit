# AudioDatasetAudit Report

## missingness
- Status: **pass**
- Summary: Calculated missing value counts and rates for all columns.
- Metrics:
  - rows: 5
  - missing_counts: {item_id=0, path=0, split=0, label=0, speaker_id=0, device_id=0, date=0, location=0, language=0, duration=0}
  - missing_rates: {item_id=0.0, path=0.0, split=0.0, label=0.0, speaker_id=0.0, device_id=0.0, date=0.0, location=0.0, language=0.0, duration=0.0}

## imbalance
- Status: **pass**
- Summary: Computed class distribution from the label column.
- Metrics:
  - class_counts: {crowd=2, market=2, car_horn=1}
  - max_to_min_ratio: 2.0
  - num_classes: 3

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
  - split_counts: {train=2, val=1, test=1, validation=1}
  - invalid_split_values: []
  - missing_core_splits: []

## speaker_id_leakage
- Status: **fail**
- Summary: Detected 1 speaker value(s) present in more than one split.
- Metrics:
  - field: speaker_id
  - rows_with_field: 5
  - unique_values: 4
  - overlap_count: 1
- Details:
  - {value=spk01, splits=['train', 'val'], num_splits=2}

## device_id_leakage
- Status: **fail**
- Summary: Detected 1 device value(s) present in more than one split.
- Metrics:
  - field: device_id
  - rows_with_field: 5
  - unique_values: 4
  - overlap_count: 1
- Details:
  - {value=phoneA, splits=['train', 'val'], num_splits=2}

## date_leakage
- Status: **fail**
- Summary: Detected 1 recording date value(s) present in more than one split.
- Metrics:
  - field: date
  - rows_with_field: 5
  - unique_values: 4
  - overlap_count: 1
- Details:
  - {value=2026-01-10, splits=['train', 'val'], num_splits=2}

## location_leakage
- Status: **fail**
- Summary: Detected 2 location value(s) present in more than one split.
- Metrics:
  - field: location
  - rows_with_field: 5
  - unique_values: 3
  - overlap_count: 2
- Details:
  - {value=accra, splits=['train', 'val'], num_splits=2}
  - {value=kumasi, splits=['test', 'val'], num_splits=2}
