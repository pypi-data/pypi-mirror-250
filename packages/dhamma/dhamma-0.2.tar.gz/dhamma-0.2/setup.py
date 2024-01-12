from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="dhamma",
    version="0.2",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "dhamma = dhamma.main:main",
        ],
    },
    description="Download and transcribe Dharma Seed retreat talks.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Daniel Posthuma",
    author_email="dnjp@posteo.org",
    url="https://github.com/dnjp/dhamma",
    install_requires=required,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
    ],
    python_requires=">=3.11",
)
