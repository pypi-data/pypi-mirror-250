from setuptools import setup, find_packages # from setuptool module iam going to import setup method or fucntion which we have defined inside this setuptool module and also find_package , and this setup methode we can get this code in setup.p
from typing import List

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()     # here iam going to open readme.md file  and read the long_description 
   

__version__ = "0.0.4"
REPO_NAME = "Mongodbconnectorpkg" # here we need to give the repository name which our packgae files and folders and its related python code present and we need to give repository name which we created in github 
PKG_NAME= "MongoDB_Database_Automation" # we need to give the package name which i given as mongodb-connector so by this name we can find our package that we uploaded in pipy
AUTHOR_USER_NAME = "Mahendra10" # # here we need to give the name of the author who is going to develop this package
AUTHOR_EMAIL = "mahendramahesh2001@gmail.com" # here we need to give the email id of the author 

setup(
    name=PKG_NAME, # here the PKG_NAME means which is package name we need to give some name for our package so by that name identity we can upload our package on top of Pipy , so here package name means tensorflow, scikit_learn which are packages names which those packages uploaded on top of Pipy by the tensorflow, scikit_learn community    
    version=__version__, # here we need to mention the version of our package and as we saw the tensorflow latest version which is released by tensorflow community on top of  Pipy 
    author=AUTHOR_USER_NAME, # here we need to give the name of the author who is going to develop this package
    author_email=AUTHOR_EMAIL, # here we need to give the email id of the author 
    description="A python package for connecting with database.", # here we need to describe with statement that the main theme of our package which we are going to upload on top of Pipy
    long_description=long_description, # here we need to give the complete details about our package so which we need write the details about of our package in long description
    long_description_content="text/markdown",  # here long description contains text as markdown which i mention this long description in some function code so that function execute the long description text which is in form of  markdown
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}", # this is my github where we can find my package files and folders which consit of python code 
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"}, # by this line we can get to know where is my package present , so its telling that my package is present inside my SRC folder which is mongodbconnecto
    packages=find_packages(where="src"),
    # install_requires=get_requirement("./requirements_dev.txt") # here iam calling the function get_requirement with its paramter as ./requirements_dev.txt  and we wrote ./ this means we are reading requirements_dev.txt  in linux syatem which is in vscode so in order to read requirements_dev.txt  current workspace  i need to write ./ by that we can able to read the file of linux system we are reading the requirements_dev.txt list which is in linux terminal
    )