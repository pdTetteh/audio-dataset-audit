from pathlib import Path

import pytest


@pytest.fixture
def sample_manifest_path() -> Path:
    return Path("tests/fixtures/sample_manifest.csv")


@pytest.fixture
def probe_manifest_path() -> Path:
    return Path("tests/fixtures/probe_manifest.csv")
