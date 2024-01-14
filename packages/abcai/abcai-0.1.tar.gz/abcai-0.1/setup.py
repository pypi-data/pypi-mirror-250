from setuptools import setup, find_packages

with open("./README.md", "r") as f:
    info = f.read()

setup(
    name="abcai",
    version="0.1",
    packages=find_packages(),
    long_description=info,
    
)
