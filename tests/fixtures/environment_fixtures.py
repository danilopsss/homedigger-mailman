import pytest
from unittest.mock import patch


@pytest.fixture(autouse=True)
def environment():
    with patch("os.getenv", return_value="test"):
        yield
