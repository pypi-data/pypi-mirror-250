from setuptools import setup, find_packages

setup(
    name='Moirepattern',
    version='0.0.2a1',
    packages=find_packages(),
    description='A lib to generate Moire patterns',
    author='IE Barrera',
    author_email='iebarrer@uc.cl',
    url = "https://github.com/funkaro1/moire-constructor",
    install_requires = ['shapely', 'PyQt5']
)