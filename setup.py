from setuptools import setup, find_packages

with open('./README.md', encoding='UTF-8') as file:
    long_description = file.read()

setup(
    name='bgplookup',
    version='0.1.1',
    python_requires=">=3.6",
    description='Command line BGP ASN lookup tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Rob W3LGA',
    author_email='RobW3LGA@github.com',
    packages=find_packages('bgplookup'),
    package_dir={'': 'bgplookup'},
    install_requires=[
        'asyncclick',
        'click',
        'httpx',
        'pydantic',
        'trio'
    ],
    entry_points={
        'console_scripts': [
            'bgplookup=main:parseCli'
        ],
    }
)