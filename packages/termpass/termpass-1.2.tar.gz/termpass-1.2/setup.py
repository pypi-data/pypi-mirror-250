from setuptools import setup

with open("README.md","r") as f:
    description = f.read()

setup(
    name='termpass',
    version='1.2',
    author='JeSeLLo',
    author_email="cebrailbilgic95@gmail.com",
    description='Gnupg based password manager',
    long_description=description,
    long_description_content_type="text/markdown",
    packages=['termpass'],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],
    install_requires=[
        'python-gnupg',
        'termcolor',
    ],
    scripts=['bin/termpass'],
) 
