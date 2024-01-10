import pathlib

import setuptools

setuptools.setup(
    name="sigmt",
    version="0.0.0",
    description="Python package for magnetotelluric data processing",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    author="Ajithabh K.S.",
    author_email="ajithabhks@gmail.com",
    url="https://github.com/ajithabhks/SigMT",
    license="GNU GENERAL PUBLIC LICENSE Version 3",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.11",
        ],
    python_requires=">=3.11",
    install_requires=["numpy>=1.24.3", 
                      "pandas>=2.0.3", 
                      "matplotlib>=3.7.2",
                      "scipy>=1.11.1",
                      "scikit-learn>=1.3.0",
                      ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={"console_scripts": ["sigmt=sigmt.cli:main"]},
    )
