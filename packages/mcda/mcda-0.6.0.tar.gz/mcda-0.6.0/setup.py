from setuptools import find_packages, setup

with open("README.PYPI.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Topic :: Scientific/Engineering :: Mathematics",
]

setup(
    name="mcda",
    version="0.6.0",
    author="Nicolas Duminy",
    author_email="nicolas.duminy@imt-atlantique.fr",
    description="Package for Multi Criteria Decision Analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Source": "https://gitlab.com/decide.imt-atlantique/pymcda",
        "Documentation": "https://py-mcda.readthedocs.io",
        "Tracker": "https://gitlab.com/decide.imt-atlantique/pymcda/issues",
    },
    classifiers=classifiers,
    package_dir={"mcda": "mcda"},
    packages=find_packages(exclude=["tests*"]),
    package_data={"": ["py.typed"]},
    test_suite="tests",
    install_requires=(
        "numpy",
        "matplotlib",
        "pulp",
        "graphviz",
        "scikit-learn",
        "pandas",
        "Deprecated",
        "typing_extensions; python_version < '3.11'",
    ),
    python_requires=">=3.8",
    zip_safe=False,
)
