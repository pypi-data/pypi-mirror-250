from setuptools import find_packages, setup


setup(
    name="puretest",
    version="0.0.1",
    description="desc",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Nikita Tsvetkov",
    author_email="tsv1@fastmail.com",
    python_requires=">=3.8",
    url="https://github.com/tsv1/puretest",
    license="Apache-2.0",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[],
    tests_require=[],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
