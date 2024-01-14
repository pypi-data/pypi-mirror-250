from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'A Python Package designed for use in the quantitative finance space'
LONG_DESCRIPTION = """

Quantpack is to be designed as a toolkit for quantitative analysis and construction of financial products.
The tool is designed from practical realworld use-cases and focuses on readablity + flexibility for users to mold the project for their needs.

"""

pkgs_dependencies = []

# Setting up
setup(
        name="quantpack", 
        version=VERSION,
        author="Rory Sullivan",
        author_email="<rorysullivan6@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=pkgs_dependencies,
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)