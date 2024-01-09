import french_highschool

from setuptools import setup, find_packages

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="django-french-highschool",
    version=french_highschool.__version__,
    description="French high school database with UAI, department and region",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/briefmnews/django-french-highschool",
    author="Brief.me",
    author_email="tech@brief.me",
    license="MIT",
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.8",
    install_requires=[
        "Django>=3.2",
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.2",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    include_package_data=True,
    zip_safe=False,
)
