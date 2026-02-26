"""
Pytest configuration and fixtures for FastAPI tests.
"""

import pytest
import copy
from src.app import activities


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Backup and restore activities dict before/after each test.
    Ensures test isolation by resetting in-memory state.
    """
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)
