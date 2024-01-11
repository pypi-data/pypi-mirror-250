

from setuptools import setup, find_packages

setup(
    # Basic package information:
    name='rolfdog',  
    version='0.0.5',
    packages=find_packages(),  # Automatically find packages in the directory

    # Dependencies:
    install_requires=[
        'numpy>=1.1.1',  
        'pandas>=0.1.1',  
    ],

    # Metadata for PyPI:
    author          ='James A. Rolfsen',
    author_email    ='james.rolfsen@think.dev', 
	description     ='Rolfdog Rolfdog Rolfdog',
	url             ='https://github.com/jrolf/rolfdog',    # Link to your repo
    
    #long_description=open('README.md').read(),
    #long_description_content_type='text/markdown',  # If your README is in markdown

    # More classifiers: https://pypi.org/classifiers/
    classifiers=[
        'Programming Language :: Python :: 3.7', 
        'License :: OSI Approved :: MIT License',  # Ensure this matches your LICENSE file
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    

)





