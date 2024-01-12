from setuptools import setup, find_packages

setup(
    name='gptbots',
    version='0.1.0',
    author='Carl Vincent Escobar',
    author_email='cvescobar112@protonmail.com',
    description='A simple Python package for creating and interacting with GPT-based chatbots',
    packages=find_packages(),
    install_requires=['openai', 'ast'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
