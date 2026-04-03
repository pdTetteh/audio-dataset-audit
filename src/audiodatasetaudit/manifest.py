from pathlib import Path

import pandas as pd

from audiodatasetaudit.schema import validate_required_columns


class ManifestError(Exception):
    pass


def load_manifest(path: str | Path) -> pd.DataFrame:
    manifest_path = Path(path)
    if not manifest_path.exists():
        raise ManifestError(f"Manifest not found: {manifest_path}")

    df = pd.read_csv(manifest_path)
    ok, missing = validate_required_columns(set(df.columns))
    if not ok:
        raise ManifestError(f"Missing required columns: {missing}")
    return df
