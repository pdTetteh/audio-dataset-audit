# AudioDatasetAudit

**Find leakage, imbalance, and metadata gaps before model training.**

AudioDatasetAudit is an open-source toolkit for auditing speech and audio datasets for leakage, imbalance, metadata gaps, split hygiene, and file-level quality issues before model training or benchmark release.

## Why this exists

Speech and audio results are often weakened by silent dataset issues such as:
- train/test leakage
- same-speaker, same-device, or same-date overlap across splits
- duplicate recordings
- severe class imbalance
- missing metadata
- inconsistent split definitions
- broken or corrupted files

AudioDatasetAudit makes these issues visible through reproducible reports.

## Current features

- manifest validation
- missing metadata analysis
- class imbalance reports
- duplicate ID and duplicate path detection
- split integrity checks
- speaker leakage detection
- device leakage detection
- date leakage detection
- location leakage detection
- JSON and Markdown reports
- CLI interface

## Planned next

- HTML reports
- audio file probing
- duration distribution summaries
- pluggable custom checks

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e '.[dev]'
```

## Quick start

Prepare a manifest CSV:

```csv
item_id,path,split,label,speaker_id,device_id,date,location,duration
001,data/a.wav,train,car_horn,spk1,phoneA,2026-01-10,accra,3.2
002,data/b.wav,val,crowd,spk1,phoneB,2026-01-11,accra,2.8
003,data/c.wav,test,market,spk3,phoneC,2026-01-12,kumasi,4.1
004,data/d.wav,validation,market,spk4,phoneA,2026-01-10,kumasi,3.9
```

Run an audit:

```bash
python3 -m audiodatasetaudit.cli examples/leaky_manifest.csv --output examples/leaky_report.md
```

Generate a JSON report:

```bash
python3 -m audiodatasetaudit.cli examples/leaky_manifest.csv --format json --output report.json
```

## Example report excerpt

Running the leaky example manifest produces failures for cross-split overlap:

```markdown
## speaker_id_leakage
- Status: **fail**
- Summary: Detected 1 speaker value(s) present in more than one split.
- Details:
  - {value=spk01, splits=['train', 'val'], num_splits=2}

## device_id_leakage
- Status: **fail**
- Summary: Detected 1 device value(s) present in more than one split.
- Details:
  - {value=phoneA, splits=['train', 'val'], num_splits=2}
```

A full sample report is included at [`examples/leaky_report.md`](examples/leaky_report.md).

## Example questions AudioDatasetAudit answers

- Are train, validation, and test splits defined correctly?
- Are some labels dramatically underrepresented?
- Are there duplicate IDs or duplicate file paths?
- Is important metadata missing for many rows?
- Are the same speakers, devices, dates, or locations leaking across splits?

## Repository layout

```text
audio-dataset-audit/
├── examples/
├── src/audiodatasetaudit/
├── tests/
├── docs/
└── notebooks/
```

## Roadmap

- **v0.1**: manifest validation, missingness, imbalance, duplicates, split integrity
- **v0.2**: leakage checks, HTML reports, visual summaries
- **v0.3**: audio probing and quality checks
- **v1.0**: stable API, plugins, public dataset examples

## Contributing

Contributions are welcome. Good first areas:
- docs improvements
- new checks
- report templates
- test cases for edge conditions
- public dataset example manifests

## License

MIT
