"""pytest fixtures for simplified testing."""
import pytest

from aiida_bigdft import helpers

pytest_plugins = ["aiida.manage.tests.pytest_fixtures"]


@pytest.fixture(scope="function", autouse=True)
def clear_database_auto(clear_database):  # pylint: disable=unused-argument
    """Automatically clear database in between tests."""


@pytest.fixture(scope="function")
def bigdft_code():
    """Get a bigdft code."""
    computer = helpers.get_computer()
    code = helpers.get_code(entry_point="bigdft", computer=computer, force_create=True)
    return code
