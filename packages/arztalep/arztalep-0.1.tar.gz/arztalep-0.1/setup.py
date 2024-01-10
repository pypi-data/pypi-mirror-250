from setuptools import setup, find_packages
setup(
    name='arztalep',
    version='0.1',
    description='Epias seffaflik sitesinden Arz Talep verilerini çeken python kutuphanesi',
    author='Tugba Ozkan',
    install_requires = ['numpy','pandas','datetime','json','requests'],
    packages=find_packages(),
)