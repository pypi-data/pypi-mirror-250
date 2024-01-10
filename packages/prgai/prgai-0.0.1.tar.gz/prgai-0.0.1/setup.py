from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'AI progs.'

# Setting up
setup(
    name="prgai",
    version=VERSION,
    author="None",
    author_email="abc@email.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pyperclip'],
    keywords=[],
    classifiers=[]
)