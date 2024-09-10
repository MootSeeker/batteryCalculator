from setuptools import setup, find_packages
from pathlib import Path

# Lies den Inhalt der README-Datei
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='batteryCalculator',  # Name deines Projekts
    version='1.0.3',  # Projektversion
    description='A battery life calculator tool',
    long_description=long_description,  # Verwende den Inhalt der README-Datei
    long_description_content_type='text/markdown',  # Gibt an, dass Markdown verwendet wird
    author='Dein Name',  # Dein Name oder Teamname
    author_email='deine.email@example.com',  # Deine E-Mail-Adresse
    packages=find_packages(),  # Automatisches Finden von Unterpaketen
    install_requires=[],  # Hier kannst du Abhängigkeiten angeben
    entry_points={
        'console_scripts': [
            'batteryCalculator = calculator:main',  # Falls du ein CLI-Tool hast
        ],
    },
)
