import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="luma-ml",
    version='0.4.6',
    author="ChanLumerico",
    author_email="greensox284@gmail.com",
    description="Custom-made powerful and light Python machine learning module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChanLumerico/LUMA",
    packages=setuptools.find_namespace_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'seaborn'
    ]
)

"""
Terminal
--------
>>> python setup.py sdist bdist_wheel
>>> python -m twine upload dist/*

PyPi Token Key
--------------
pypi-AgEIcHlwaS5vcmcCJDNiY2JhODE4LWRkYmUtNDliYi1iMTY3LTlhMGVkZjI4NTk2Zg
ACD1sxLFsibHVtYS1tbCJdXQACLFsyLFsiNTA2NmE0N2ItYzY1Yi00ZDNiLWIwZGQtZjNmZ
TgxNzgwMDQwIl1dAAAGIIisjSem6u8yAueOO3tuP2fS8oPI0x3WQTM-Y5EGe8C4

"""
