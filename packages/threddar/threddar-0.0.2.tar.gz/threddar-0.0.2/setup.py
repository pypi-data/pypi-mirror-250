from setuptools import setup, find_packages

setup(
    name='threddar',
    version='0.0.1',
    author='S. C. The Mysterious',
    author_email='moo.no.email@cow.com',
    description='Allows you to create special thread groups',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)