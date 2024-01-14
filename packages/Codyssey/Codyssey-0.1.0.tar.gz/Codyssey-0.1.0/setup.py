from setuptools import setup, find_packages

setup(
    name='Codyssey',
    version='0.1.0',
    packages=find_packages(),
    description='Python arsenal for competitive mastery',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Kanishk Varshney',
    author_email='varskann1993@gmail.com',
    url='https://github.com/varskann/Codyssey',
    install_requires=[
        'typing',
        'typing_extensions',
    ],
    classifiers=[
        # Classifiers help users find your project
        # Refer to the Python Packaging User Guide for the complete list
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
