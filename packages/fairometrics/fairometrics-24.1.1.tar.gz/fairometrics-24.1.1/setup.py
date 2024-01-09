from setuptools import setup
import os
from pathlib import Path


def get_long_description():
    # read the contents of your README file
    this_directory = Path(__file__).parent
    long_description = (this_directory / "README.md").read_text()
    return long_description


def extract_tag_release_id():
    # Get the full reference from the environment variable
    full_ref = os.getenv('GITHUB_REF')

    # Check if the GITHUB_REF is set and it's a tag
    if full_ref and full_ref.startswith('refs/tags/'):
        # Extract the tag name
        tag_name = full_ref.split('/')[-1]
        return tag_name.replace('release-v', '')
    else:
        return ""


setup(
    name="fairometrics",
    version=extract_tag_release_id(),
    author="Fairo Systems, Inc.",
    author_email="support@fairo.ai",
    description=("A collection of pre-certified fairness metrics supported by Fairo."),
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    license="Apache-2.0",
    keywords="fairo fairness AI governance metrics",
    url="https://www.fairo.ai",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=['fairometrics'],
    install_requires=[],
)
