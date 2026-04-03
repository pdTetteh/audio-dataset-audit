# Examples

## Leakage example

Generate the HTML report:

```bash
python3 -m audiodatasetaudit.cli examples/leaky_manifest.csv --format html --output examples/leaky_report.html
```

## File-level probing example

Generate the HTML report:

```bash
python3 -m audiodatasetaudit.cli examples/probe_manifest.csv --format html --output examples/probe_report.html
```

The probe example demonstrates:
- a missing file
- an unreadable audio file
- mixed sample rates
- mixed channel counts
- a very short file
- a manifest duration mismatch
