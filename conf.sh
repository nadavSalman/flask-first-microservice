#!/bin/bash

# Source doc : https://auth0.com/blog/developing-restful-apis-with-python-and-flask/ 
# Pipenv is a dependency manager that isolates projects in private environments, allowing packages to be installed per project. 
pip install pipenv

# create our project directory and move to it
mkdir cashman-flask-project && cd cashman-flask-project

# use pipenv to create a Python 3 (--three) virtualenv for our project
pipenv --three

# install flask a dependency on our project
pipenv install flask

# If we check our project's directory, we will see two new files:

# Pipfile contains details about our project, such as the Python version and the packages needed.
# Pipenv.lock contains precisely what version of each package our project depends on and its transitive dependencies.


# Python modules


# To create a module on a Python application, we need to create a folder and add an empty file called __init__.py.