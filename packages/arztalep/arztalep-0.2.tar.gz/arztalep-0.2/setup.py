from setuptools import setup, find_packages
setup(
    name='arztalep',
    version='0.2',
    description='Epias seffaflik sitesinden Arz Talep verilerini çeken python kutuphanesi',
    author='Tugba Ozkan',
    install_requires = ['numpy','pandas','datetime','requests'],
    packages=find_packages(),
)