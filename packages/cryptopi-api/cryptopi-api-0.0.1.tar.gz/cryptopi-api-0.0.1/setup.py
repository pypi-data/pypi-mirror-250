from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "A simple Flask API for the `cryptopi` package."

setup(
    name="cryptopi-api",
    version=VERSION,
    author="Jake Williamson",
    author_email="<brianjw88@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "cryptopi",
        "pydantic",
        "uvicorn",
    ],
    keywords=["python", "crypto", "api", "coinmarketcap", "coinmarketcap-api"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
)