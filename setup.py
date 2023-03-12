from setuptools import find_packages, setup
from typing import List

REQUIREMENT_FILE_NAME = "requirements.txt"
HYPHEN_E_DOT = "-e ."


def get_requirements()->List[str]:
    """
    This function will return all the packages available in requirements.txt as a list
    """
    with open(REQUIREMENT_FILE_NAME) as requirement_file_name:
        requirement_list = requirement_file_name.readlines()
    requirement_list = [requirement_package.replace('\n','') for requirement_package in requirement_list]
    if HYPHEN_E_DOT in requirement_list:
        requirement_list.remove(HYPHEN_E_DOT)
    return requirement_list

setup(
    name="restraunt-rating-prediction",
    version="0.0.1",
    author="Rahul Chatterjee",
    author_email="chatterjeerahul187@gmail.com",
    packages=find_packages(),
    install_requires = get_requirements()

)