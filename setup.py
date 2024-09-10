from setuptools import setup, find_packages

setup(
    name='batteryCalculator',  # Name deines Projekts
    version='1.0.3',  # Projektversion
    description='A battery life calculator tool',
    author='MootSeeker',  # Dein Name oder Teamname
    author_email='mootseeker98@gmail.com',  # Deine E-Mail-Adresse
    packages=find_packages(),  # Automatisches Finden von Unterpaketen
    install_requires=[],  # Hier kannst du Abhängigkeiten angeben, z.B. ['tkinter', 'numpy']
    entry_points={
        'console_scripts': [
            'batteryCalculator = calculator:main',  # Falls du ein CLI-Tool hast
        ],
    },
)
