# setup.py

from setuptools import setup, find_packages

setup(
    name='JoyMondalSIG',
    version='0.1',
    packages=find_packages(),
    author='Joy Mondal',
    author_email='Contact.Joymondal@email.com',
    description='A Python package to gather system information and check Python installation.',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    url='https://github.com/codewithjoymondal/JoyMondalSIG',
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
