import importlib
from copy import deepcopy
import pytest

# Import the application module so we can access and restore its in-memory state
app_module = importlib.import_module("src.app")


@pytest.fixture(autouse=True)
def reset_activities():
    """Backup and restore the in-memory `activities` dict around each test.

    Uses autouse=True so tests don't need to opt in; this ensures isolation
    following the Arrange-Act-Assert pattern.
    """
    original = deepcopy(app_module.activities)
    try:
        yield
    finally:
        app_module.activities.clear()
        app_module.activities.update(original)
