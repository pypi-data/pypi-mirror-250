from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
        name = "bibchk",
        version = "0.2.0",
        author = "Doug Keller",
        author_email = "dg.kllr.jr@gmail.com",
        description = "Simple command line program to return the BibTeX string of a given DOI or ISBN.",
        long_description = long_description,
        long_description_content_type = "text/markdown",
        url = "https://github.com/BibTheque/bibchk",
        package_dir={"": "src"},
        python_requires = ">=3.9",
        packages=find_packages(where="src"),
        install_requires = [
            'click',
            'bibtexparser',
            'habanero',
            'isbnlib',
        ],
        entry_points = {
            'console_scripts': [
                'bibchk = bibchk.cli:bibchk',
            ]

        },
        classifiers = [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
            "Operating System :: OS Independent",
        ],
)
