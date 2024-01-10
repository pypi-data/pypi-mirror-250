from setuptools import setup, find_packages

setup(
    name='arlingo',
    version='0.3.12',
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4",
        "easygoogletranslate",
        "gtts",
        "pydub"
    ],
)
