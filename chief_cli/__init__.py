"""Chief CLI — Application management from your terminal."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("chief-cli")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"
