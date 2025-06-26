"""
Setup script for Architex.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Read requirements
requirements = (this_directory / "requirements.txt").read_text().splitlines()

setup(
    name="architex",
    version="0.1.0",
    author="Architex Team",
    author_email="team@architex.dev",
    description="Automated System Design Diagram Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/architex",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "architex=architex.cli.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "architex": ["*.json", "*.yaml", "*.yml"],
    },
    keywords="architecture, diagram, code analysis, system design, visualization",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/architex/issues",
        "Source": "https://github.com/yourusername/architex",
        "Documentation": "https://architex.readthedocs.io",
    },
) 