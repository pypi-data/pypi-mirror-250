from setuptools import setup, find_packages

setup(
    name="cooleans",
    version="0.2.0",
    author="Aymeric Gaillard",
    author_email="aymeric.gaillard@protonmail.com",
    description="Better than booleans",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="type bool booleans perhaps",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)