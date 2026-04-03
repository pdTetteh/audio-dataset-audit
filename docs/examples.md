# Examples

## Minimal manifest

Use `examples/minimal_manifest.csv` when you want a clean starter manifest with no expected failures.

## Leaky manifest

Use `examples/leaky_manifest.csv` when you want to demonstrate cross-split leakage detection.

Run:

```bash
python3 -m audiodatasetaudit.cli examples/leaky_manifest.csv --output examples/leaky_report.md
```

This example intentionally triggers failures for:
- `speaker_id_leakage`
- `device_id_leakage`
- `date_leakage`
- `location_leakage`

The generated sample output lives in `examples/leaky_report.md`.
