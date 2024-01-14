from setuptools import setup,find_packages
import pathlib

setup(
    name='avinashtare_hello',
    version="1.2.0",
    install_requires=[
        # numpy>=1.11.1
    ],
    entry_points={
        "console_scripts": [
            "avinash = avinashtare_hello:PrintText"
        ]
    },
    author="avinash developer",
    description="Short Description",
    
    long_description=pathlib.Path("README.md").read_text(),
    author_email="avinashtare55.dummy@gmail.com",
    url="https://avinashtare.online",
    license=pathlib.Path("LICENCE").read_text(),
    project_urls={
        "documentation": "https://india.com",
        "Source":"https://github.com/avinashtare",
    },
)