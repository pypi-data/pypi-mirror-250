import setuptools
import os

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()




setuptools.setup(
    name="database_connect",
    version="0.1.671",
    author="Hrisikesh Neogi",
    author_email="hrisikesh.neogi@gmail.com",
    description="A single Package for all the database connectivities  ( E.g : MySQL, MongoDb, Cassandra)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hrisikesh-neogi/Database-Connect",
    project_urls={
        "Bug Tracker": "https://github.com/hrisikesh-neogi/Database-Connect/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
        "cassandra-driver==3.29.0",
        "ensure==1.0.4",
        "pandas==2.0.3",
        "pymongo==4.6.1",
        "pymongo[srv]",
    ],
)
