"""Setup configuration for watermark-pdf-tool.

This setup.py is maintained for backward compatibility and to support
dynamic version reading from the package.
"""

from setuptools import setup

# Read version from package
def get_version():
    """Read version from watermark_pdf_tool/__init__.py"""
    version = {}
    with open("watermark_pdf_tool/__init__.py") as fp:
        for line in fp:
            if line.startswith("__version__"):
                exec(line, version)
                return version["__version__"]
    raise RuntimeError("Unable to find version string.")

setup(
    version=get_version(),
)
