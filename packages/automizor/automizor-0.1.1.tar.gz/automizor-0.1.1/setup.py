from setuptools import setup, find_packages

from automizor import version


setup(
    name="automizor",
    version=version,
    description="Python Automizor framework",
    url="https://github.com/vcodx/automizor",
    author="Christian Fischer",
    author_email="christian@vcodx.com",
    license="Apache License",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="automizor framework",
    packages=find_packages(include=["automizor", "automizor.*"]),
    include_package_data=True,
)
