REQUIRED_COLUMNS = {"item_id", "path", "split", "label"}
OPTIONAL_COLUMNS = {
    "speaker_id",
    "device_id",
    "collector_id",
    "date",
    "location",
    "language",
    "duration",
    "sample_rate",
    "channels",
    "source_dataset",
}


def validate_required_columns(columns: set[str]) -> tuple[bool, list[str]]:
    missing = sorted(REQUIRED_COLUMNS - columns)
    return len(missing) == 0, missing
