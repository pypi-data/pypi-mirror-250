from setuptools import setup, find_packages

setup(
    name="psifospoll",
    version="1.0.0",
    author="Fernanda Macías",
    author_email="fernanda.macias@ug.uchile.cl",
    description="PsifosPoll is a python library for different voting methods",
    packages=find_packages(),
    url="https://github.com/clcert/psifospoll",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
