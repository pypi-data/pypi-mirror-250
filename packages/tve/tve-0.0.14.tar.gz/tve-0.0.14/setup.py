from io import open
from setuptools import setup

version = '0.0.14'

setup(
    name = 'tve',
    version=version,

    author='Lohi',
    author_email='usaidoleg@gmail.com',

    license='Free' ,
    
    include_package_data=True,
    
    packages= ['tve']
)