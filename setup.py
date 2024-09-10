from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='batteryCalculator',  
    version='1.0.3',  
    description='A battery life calculator tool',
    long_description=long_description, 
    long_description_content_type='text/markdown',  
    author='MootSeeker',  
    author_email='mootseeker98@gmail.com', 
    packages=find_packages(),  
    install_requires=[],  
    entry_points={
        'console_scripts': [
            'batteryCalculator = calculator:main',  
        ],
    },
)
