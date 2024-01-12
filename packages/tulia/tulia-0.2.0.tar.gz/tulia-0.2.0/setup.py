from setuptools import setup, find_packages

VERSION = '0.2.0'
DESCRIPTION = 'numpy based machine learning package with sklearn-like API'

with open("README.md", "r") as fn:
    long_description = fn.read()

setup(
    name="tulia",
    version=VERSION,
    author="Valentin Belyaev",
    author_email="chuvalik.work@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    url="https://github.com/chuvalniy/tulia",
    install_requires=['numpy', 'pytest'],
    license="MIT",
    keywords=['python', 'machine learning', 'from scratch', 'numpy', 'sklearn-like', 'random forest', 'tree', 'knn'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)