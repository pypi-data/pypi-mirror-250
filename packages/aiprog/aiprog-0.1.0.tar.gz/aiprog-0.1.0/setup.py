from setuptools import setup, find_packages

VERSION = '0.1.0'
DESCRIPTION = 'AI progs.'

# Setting up
setup(
    name="aiprog",
    version=VERSION,
    author="None",
    author_email="mohits.reddy@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pyperclip'],
    keywords=[],
    classifiers=[]
)