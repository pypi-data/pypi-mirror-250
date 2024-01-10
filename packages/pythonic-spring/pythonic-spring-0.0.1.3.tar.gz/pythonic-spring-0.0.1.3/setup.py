from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="pythonic-spring",
    version="0.0.1.3",
    description="A python-made framework which is like Spring in Java.",
    author="Tianhao Zhang",
    author_email="genji9071@gmail.com",
    license="MIT",
    keywords="spring pythonic",
    project_urls={
        "Source": "https://github.com/genji9071/pythonic-spring/",
        "Tracker": "https://github.com/genji9071/pythonic-spring/issues"
    },
    packages=find_packages(),
    install_requires=["fastapi~=0.108.0", "setuptools~=65.5.1", "pydantic~=2.5.3"],
    python_requires=">=3.7",
    long_description=long_description,
    long_description_content_type='text/markdown'
)