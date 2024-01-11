from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='tileclipper',
    version='0.5',
    packages=find_packages(),
    package_data={'tileclipper': ['README.md', 'docs/*.md', 'LICENSE']},
    install_requires=[
        'requests',
        'pyproj'
        # Add other dependencies here if needed
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)