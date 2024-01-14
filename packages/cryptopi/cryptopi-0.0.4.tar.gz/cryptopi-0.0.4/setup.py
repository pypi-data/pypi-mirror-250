from setuptools import setup, find_packages

VERSION = "0.0.4"
DESCRIPTION = "A simple python wrapper for Coin Market Cap API"

setup(
    name="cryptopi",
    version=VERSION,
    author="Jake Williamson",
    author_email="<brianjw88@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        "requests",
        "pydantic",
    ],
    keywords=["python", "crypto", "api", "coinmarketcap", "coinmarketcap-api"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
)
