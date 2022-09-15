from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Utilities'
LONG_DESCRIPTION = 'Utilities for data manipulation and analysis'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="dsutils", 
        version=VERSION,
        author="Elisa Lubrini",
        author_email="<lubrinie@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'utils', 'visualisation'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            'Operating System :: POSIX',
        ]
)