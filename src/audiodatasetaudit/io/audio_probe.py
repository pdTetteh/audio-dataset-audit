from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import soundfile as sf


@dataclass(frozen=True)
class AudioProbeResult:
    raw_path: str
    resolved_path: str
    exists: bool
    readable: bool
    sample_rate: int | None = None
    channels: int | None = None
    frames: int | None = None
    duration: float | None = None
    format: str | None = None
    subtype: str | None = None
    error: str | None = None


def resolve_audio_path(raw_path: str, base_dir: Path | None = None) -> Path:
    candidate = Path(raw_path).expanduser()
    if candidate.is_absolute() or base_dir is None:
        return candidate
    return (base_dir / candidate).resolve()


def probe_audio_file(raw_path: str, base_dir: Path | None = None) -> AudioProbeResult:
    resolved = resolve_audio_path(raw_path, base_dir)
    if not resolved.exists():
        return AudioProbeResult(
            raw_path=raw_path,
            resolved_path=str(resolved),
            exists=False,
            readable=False,
            error="file_not_found",
        )

    try:
        info = sf.info(str(resolved))
    except Exception as exc:  # pragma: no cover - library error text can vary by platform
        return AudioProbeResult(
            raw_path=raw_path,
            resolved_path=str(resolved),
            exists=True,
            readable=False,
            error=str(exc),
        )

    return AudioProbeResult(
        raw_path=raw_path,
        resolved_path=str(resolved),
        exists=True,
        readable=True,
        sample_rate=int(info.samplerate),
        channels=int(info.channels),
        frames=int(info.frames),
        duration=float(info.duration),
        format=info.format,
        subtype=info.subtype,
        error=None,
    )


def probe_manifest_paths(
    df: pd.DataFrame,
    base_dir: Path | None = None,
) -> dict[str, AudioProbeResult]:
    if "path" not in df.columns:
        return {}

    paths = (
        df["path"]
        .dropna()
        .astype("string")
        .str.strip()
    )
    unique_paths = [str(path) for path in paths if path]
    return {path: probe_audio_file(path, base_dir) for path in dict.fromkeys(unique_paths)}
