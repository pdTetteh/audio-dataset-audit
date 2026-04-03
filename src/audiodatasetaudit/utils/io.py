from pathlib import Path


def ensure_parent_dir(path: str | Path) -> None:
    Path(path).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)
