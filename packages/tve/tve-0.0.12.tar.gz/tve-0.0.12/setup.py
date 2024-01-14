from io import open
from setuptools import setup

version = '0.0.12'

setup(
    name = 'tve',
    version=version,

    author='Lohi',
    author_email='usaidoleg@gmail.com',

    license='Free' ,
    
    include_package_data=True,
    
    packages= ['tve']
)