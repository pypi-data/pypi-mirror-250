from setuptools import setup, find_packages
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

with open(this_directory / 'requirements.txt',encoding='utf-16') as f:
    requirements = f.read().splitlines()

setup(
    name='pyrpasuite',  
    version='0.0.1',  
    author='Muktadir',  
    long_description=long_description,
    long_description_content_type='text/markdown',
    description='RPA using python',  
    packages=find_packages(),  
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',  
    ],
)
