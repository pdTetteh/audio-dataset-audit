# ruff: noqa: B008
from __future__ import annotations

from pathlib import Path

import typer
from rich import print

from audiodatasetaudit.checks.audio_readability import AudioReadabilityCheck
from audiodatasetaudit.checks.base import AuditCheck
from audiodatasetaudit.checks.channel_consistency import ChannelConsistencyCheck
from audiodatasetaudit.checks.duplicates import DuplicateCheck
from audiodatasetaudit.checks.duration import DurationCheck
from audiodatasetaudit.checks.file_existence import FileExistenceCheck
from audiodatasetaudit.checks.imbalance import ImbalanceCheck
from audiodatasetaudit.checks.leakage import LeakageCheck
from audiodatasetaudit.checks.missingness import MissingnessCheck
from audiodatasetaudit.checks.sample_rate import SampleRateConsistencyCheck
from audiodatasetaudit.checks.split_integrity import SplitIntegrityCheck
from audiodatasetaudit.io.audio_probe import probe_manifest_paths
from audiodatasetaudit.manifest import load_manifest
from audiodatasetaudit.reports.html_report import write_html_report
from audiodatasetaudit.reports.json_report import write_json_report
from audiodatasetaudit.reports.markdown_report import write_markdown_report

app = typer.Typer(help="Audit speech and audio datasets for common quality risks.")


def _build_checks(manifest_dir: Path, df) -> list[AuditCheck]:
    probe_results = probe_manifest_paths(df, manifest_dir)
    return [
        MissingnessCheck(),
        ImbalanceCheck(),
        DuplicateCheck(),
        SplitIntegrityCheck(),
        LeakageCheck("speaker_id", "speaker"),
        LeakageCheck("device_id", "device"),
        LeakageCheck("date", "recording date"),
        LeakageCheck("location", "location"),
        FileExistenceCheck(probe_results),
        AudioReadabilityCheck(probe_results),
        SampleRateConsistencyCheck(probe_results),
        ChannelConsistencyCheck(probe_results),
        DurationCheck(probe_results),
    ]


@app.command()
def audit(
    manifest: Path = typer.Argument(..., help="Path to manifest CSV."),
    report_format: str = typer.Option(
        "markdown", "--format", help="Report format: markdown, json, or html."
    ),
    output: Path | None = typer.Option(None, help="Output report path."),
) -> None:
    df = load_manifest(manifest)
    checks = _build_checks(manifest.parent.resolve(), df)
    results = [check.run(df) for check in checks]

    print(f"[bold green]Loaded[/bold green] {len(df)} rows from {manifest}")
    for result in results:
        print(f"- {result.name}: {result.status}")

    if output is not None:
        if report_format == "json":
            write_json_report(results, str(output))
        elif report_format == "markdown":
            write_markdown_report(results, str(output))
        elif report_format == "html":
            write_html_report(results, str(output))
        else:
            raise typer.BadParameter("format must be one of: markdown, json, html")
        print(f"[bold blue]Report written to[/bold blue] {output}")


if __name__ == "__main__":
    app()
