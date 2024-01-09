from setuptools import setup, find_packages
from package.version import version


# Function to read the list of dependencies from requirements.txt
def read_requirements():
    with open('./requirements.txt') as req:
        return req.read().splitlines()


# Function to read the README file
def read_readme():
    with open('README.md', 'r') as readme:
        return readme.read()


setup(
    name="codara",
    version=version,
    packages=find_packages(),
    description="AI Code Review Automation Tool",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "codara=package.app:main"
        ]
    }
)
