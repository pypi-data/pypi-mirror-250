from setuptools import setup, find_packages

setup(
    name='demommath',
    version='0.1.6',
    packages=find_packages(),
    long_description_content_type="text/markdown",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'your-command-name=your_package.module1:main_function',
        ],
    },
    author='Gangesh',
    author_email='gvelip@nio.org',
    description='This package is for testing And How to create a package',

)

