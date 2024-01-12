from setuptools import setup, find_packages

setup(
    name='mypackage',
    version='0.1.5',
    author='Carl Vincent Escobar',
    author_email='cvescobar112@protonmail.com',
    description='A simple Python package for creating and interacting with GPT-based chatbots',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
