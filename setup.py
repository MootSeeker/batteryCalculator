from setuptools import setup

APP = ['batteryCalculator.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['batteryCalculator'],  # Ersetze 'your_package' durch den Namen deines Pakets, falls erforderlich
    'iconfile': 'icon.icns',  # optional
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
