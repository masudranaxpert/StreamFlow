from streamflow import __version__
from streamflow.constants import PACKAGE_VERSION


def test_version() -> None:
    assert __version__ == PACKAGE_VERSION
