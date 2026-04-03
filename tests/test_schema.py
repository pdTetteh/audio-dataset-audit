from audiodatasetaudit.schema import validate_required_columns


def test_validate_required_columns_success() -> None:
    ok, missing = validate_required_columns({"item_id", "path", "split", "label"})
    assert ok is True
    assert missing == []


def test_validate_required_columns_missing() -> None:
    ok, missing = validate_required_columns({"item_id", "path"})
    assert ok is False
    assert "split" in missing
    assert "label" in missing
