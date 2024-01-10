from setuptools import find_packages, setup

requirements = """
pip>=21.3.1
setuptools>=56
pandas
coverage
python-dotenv
click==7.1.2
deepdiff
gitpython
requests
"""

description = """
Python package to manipulate Snowsight worksheets
 and easily apply Git versioning on it.
"""

setup(
    name="sf_git",
    setup_requires=["setuptools_scm"],
    # use_scm_version={
    #     "write_to": "version.txt",
    #     "root": ".",
    #     "relative_to": __file__,
    # },
    version="1.0",
    author="Thomas Dambrin",
    author_email="thomas.dambrin@gmail.com",
    description=description,
    packages=find_packages(),
    install_requires=requirements,
    keywords=["python", "snowflake", "git"],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ],
    # include_package_data: to install data from MANIFEST.in
    include_package_data=True,
    zip_safe=False,
    # all functions @cli.command() decorated in sf_git/cli.py
    entry_points={"console_scripts": ["sfgit = sf_git.cli:cli"]},
    scripts=[],
)
