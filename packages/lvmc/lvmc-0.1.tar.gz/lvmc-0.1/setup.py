from setuptools import setup, find_packages

setup(
    name="lvmc",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
        "tqdm",
        "torch",
    ],
    author="EL KHIYATI Zakarya",
    author_email="zakaryaelkhiyati@gmail.com",
    description="A package for simulating Vicsek-like particles on a 2D lattice with magnetic fields",
)
