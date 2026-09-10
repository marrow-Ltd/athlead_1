import pytest


@pytest.mark.skip(reason="Requires a configured test database — see README for setup.")
def test_csv_upload_rejects_missing_fields():
    pass
