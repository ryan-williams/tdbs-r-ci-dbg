from setuptools import setup, find_packages


setup(
    name="tdbs-r-ci-dbg",
    packages=find_packages(),
    install_requires=open("requirements.txt").read(),
    entry_points={
        "console_scripts": [
            "dbg-r-ci = cli.main:cli",
        ]
    },
)
