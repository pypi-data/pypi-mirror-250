"""
Build the wheel file for the library luminex.
"""

from setuptools import find_packages, setup
import sys

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

def get_version():
    """
    Checks commandline arguments for a user specified Version number.
    If the --version flag is not given at run time, then the version number is defaulted to
    v0.0.2, which will later be replaced with a git tag when performing
    version releases.

    Returns
    -------
    when the bdist_wheel command is given a version flag and version number, such as:

    --version 1.x.x

    the version of the built whl file will include the given version number, such as:

    luminex-1.x.x-py3-none-any.whl


    Error Handling
    --------------
    If the --version flag is given, but no version number is supplied, such as:

    --version

    then an IndexError will be thrown and the build will exit with exit status 1.

    """
    version = 'v0.0.2'
    if "--version" in sys.argv:
        try:
            version = sys.argv[3]
            sys.argv.remove(sys.argv[3])
        except IndexError as e:
            print("error:  " + str(e))
            print("supply a version number i.e. --version 1.x.x")
            exit(1)
        sys.argv.remove("--version")
    return version


version_var = str(get_version())

setup(
    name='luminex',
    version=version_var,
    description='On the Fly ETL application',
    url='',
    author_email='devex@dish.com',
    license='Dish Wireless',
    packages=find_packages(
        include=['luminex',
                 'luminex.data_standardization',
                 'luminex.validation'
                 ]
    ),
    include_package_data=True,
    install_requires=[
        'pyspark',
        'pandas',
        'numpy',
        'boto3',
        'fastparquet',
        'pyarrow',
        'python-dotenv',
        'requests',
        'pyyaml',
        'PyGithub'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
    )