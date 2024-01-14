from io import open
from setuptools import setup

version = '0.0.24'

setup(
    name = 'tve',
    version=version,

    author='Lohi',
    author_email='usaidoleg@gmail.com',

    license='Free' ,

    include_package_data=True,  # Include data files specified in MANIFEST.in
    
    package_data={
        '': ['pic/*.png'],  # Include all PNG files in the 'pic' directory
    },
    
    packages= ['tve']
)