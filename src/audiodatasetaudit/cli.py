from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich import print

from audiodatasetaudit.checks.base import AuditCheck
from audiodatasetaudit.checks.duplicates import DuplicateCheck
from audiodatasetaudit.checks.imbalance import ImbalanceCheck
from audiodatasetaudit.checks.leakage import LeakageCheck
from audiodatasetaudit.checks.missingness import MissingnessCheck
from audiodatasetaudit.checks.split_integrity import SplitIntegrityCheck
from audiodatasetaudit.manifest import load_manifest
from audiodatasetaudit.reports.json_report import write_json_report
from audiodatasetaudit.reports.markdown_report import write_markdown_report

app = typer.Typer(help="Audit speech and audio datasets for common quality risks.")

ManifestArg = Annotated[Path, typer.Argument(..., help="Path to manifest CSV.")]
FormatOption = Annotated[
    str, typer.Option("markdown", help="Report format: markdown or json.")
]
OutputOption = Annotated[Path | None, typer.Option(None, help="Output report path.")]


def _build_checks() -> list[AuditCheck]:
    return [
        MissingnessCheck(),
        ImbalanceCheck(),
        DuplicateCheck(),
        SplitIntegrityCheck(),
        LeakageCheck("speaker_id", "speaker"),
        LeakageCheck("device_id", "device"),
        LeakageCheck("date", "recording date"),
        LeakageCheck("location", "location"),
    ]


@app.command()
def audit(
    manifest: ManifestArg,
    format: FormatOption = "markdown",
    output: OutputOption = None,
) -> None:
    df = load_manifest(manifest)
    results = [check.run(df) for check in _build_checks()]

    print(f"[bold green]Loaded[/bold green] {len(df)} rows from {manifest}")
    for result in results:
        print(f"- {result.name}: {result.status}")

    if output is not None:
        if format == "json":
            write_json_report(results, str(output))
        elif format == "markdown":
            write_markdown_report(results, str(output))
        else:
            raise typer.BadParameter("format must be one of: markdown, json")
        print(f"[bold blue]Report written to[/bold blue] {output}")


if __name__ == "__main__":
    app()