from setuptools import setup, find_packages
from pathlib import Path


readme_path = Path(__file__).parent
readme = (readme_path / "README.md").read_text()

setup (
    name="nerimity",
    version="1.5.1",
    packages=find_packages(),
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=[
        "aiohttp>=3.11.13",
        "websockets>=15.0.1",
        "requests>=2.32.3"
    ]

)