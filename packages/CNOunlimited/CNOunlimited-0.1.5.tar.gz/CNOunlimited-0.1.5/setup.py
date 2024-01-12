from setuptools import setup, find_packages

setup(
    name='CNOunlimited',
    version='0.1.5',
    author='Dustin Cocherell',
    author_email='dcocherell@choctawnation.com',
    description='This package is designed to assist with common task that CNO Enterprise Application Engineering team performs, preventing repetitive code and increasing efficiency.',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)