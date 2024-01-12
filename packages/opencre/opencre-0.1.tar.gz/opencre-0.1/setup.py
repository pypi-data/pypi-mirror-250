from setuptools import setup, find_packages

setup(
    name='opencre',
    version='0.1',
    author='Caleb Lewallen',
    author_email='caleb@lewallen.io',
    description='A package of basic calculations and functions commonly used in Commercial Real Estate',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 1 - Planning'
    ],
    python_requires='>=3.10',
)