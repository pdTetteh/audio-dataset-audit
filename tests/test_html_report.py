from pathlib import Path

import pandas as pd

from audiodatasetaudit.checks.duplicates import DuplicateCheck
from audiodatasetaudit.checks.imbalance import ImbalanceCheck
from audiodatasetaudit.checks.leakage import LeakageCheck
from audiodatasetaudit.checks.missingness import MissingnessCheck
from audiodatasetaudit.checks.split_integrity import SplitIntegrityCheck
from audiodatasetaudit.reports.html_report import write_html_report

LEAKY_MANIFEST = Path("tests/fixtures/leaky_manifest.csv")


def test_write_html_report_creates_expected_sections(tmp_path: Path) -> None:
    df = pd.read_csv(LEAKY_MANIFEST)
    results = [
        MissingnessCheck().run(df),
        ImbalanceCheck().run(df),
        DuplicateCheck().run(df),
        SplitIntegrityCheck().run(df),
        LeakageCheck("speaker_id", "speaker").run(df),
    ]
    output_path = tmp_path / "report.html"

    write_html_report(results, str(output_path))

    html = output_path.read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in html
    assert "AudioDatasetAudit Report" in html
    assert "summary-grid" in html
    assert "speaker_id_leakage" in html
    assert "spk01" in html
    assert "status-fail" in html
    assert "Metrics" in html
    assert "Details" in html
