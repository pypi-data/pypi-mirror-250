"""Setup for trusted-ai package."""
from setuptools import find_packages, setup
import toml
 
with open('pyproject.toml', 'r') as f:
    config = toml.load(f)

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="trusted-ai",
    version=config['project']['version'],
    description=config['project']['description'],
    author=config['project']['authors'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(include=["tai", "tai.*"]),
    include_package_data=True,
    install_requires=config['project']['dependencies'],
    data_files=[("", ["VERSION"])],
    python_requires=config['project']['requires-python'],
)
