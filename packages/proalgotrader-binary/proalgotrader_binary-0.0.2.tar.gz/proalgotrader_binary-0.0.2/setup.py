import os

from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt") as fp:
    install_requires = fp.read().strip().split("\n")


def get_directories_recursive(base_path: str) -> list:
    directories = [base_path]

    for root, dirs, files in os.walk(base_path):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            package = dir_path.replace(os.path.sep, ".")
            directories.append(package)

    return directories


setup(
    name="proalgotrader_binary",
    version="0.0.2",
    description="ProAlgoTrader core",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/krunaldodiya/proalgotrader_core",
    author="Krunal Dodiya",
    author_email="kunal.dodiya1@gmail.com",
    packages=get_directories_recursive("proalgotrader_binary"),
    package_data={"": ["*"]},
    include_package_data=True,
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
