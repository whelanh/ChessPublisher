"""
Setup configuration for Chess Diagram Generator
For packaging and distribution
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="chess-diagram-generator",
    version="1.0.0",
    author="Hugh Whelan",
    author_email="brickhousedevelopers@gmail.com",
    description="Generate publication-ready chess diagrams and annotated games using LaTeX",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/whelanh/ChessPublisher",
    py_modules=["chess_generator"],
    install_requires=[
        "chess>=1.10.0",
    ],
    extras_require={
        'dev': [
            'pytest>=7.0',
            'black>=22.0',
            'mypy>=0.950',
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment :: Board Games",
        "Topic :: Text Processing :: Markup :: LaTeX",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    keywords="chess diagrams latex pdf publishing texlive pgn fen",
    project_urls={
        "Bug Reports": "https://github.com/whelanh/ChessPublisher/issues",
        "Documentation": "https://github.com/whelanh/ChessPublisher#readme",
        "Source": "https://github.com/whelanh/ChessPublisher",
    },
    include_package_data=True,
    package_data={
        '': ['bin/**/*', 'examples/*.py'],
    },
)
