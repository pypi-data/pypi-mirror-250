from setuptools import setup, find_packages

setup(
    name="closehaven-abc",
    version="0.1.1",
    packages=find_packages(),
    install_requires = [
        'fastapi==0.103.2',
        'pydantic==2.4.2',
        'azure-storage-blob==12.19.0'
    ]
)
