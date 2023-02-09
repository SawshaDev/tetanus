import re
from pathlib import Path

from setuptools import setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

path = Path(__file__).parent / "wharf" / "__init__.py"
version = re.search(r"\d[.]\d[.]\d", path.read_text())

if not version:
    raise RuntimeError('version is not set')

version = version[0]
packages = ["tetanus", "tetanus.impl", "tetanus.models", "tetanus.types"]


setup(
    name="tetanus",
    author="SawshaDev",
    version=version,
    packages=packages,
    license="MIT",
    description="a simple api wrapper for eludris",
    install_requires=requirements,
    python_requires=">=3.8.0",
)
