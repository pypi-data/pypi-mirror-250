from setuptools import setup, find_packages
import pathlib

# read the contents of your README file
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='quacker',
    version='0.6.1',
    description='Sync dbt sources and models from cloud warehouses to duckdb',  # Short description
    long_description=long_description,  # Long description read from the README.md
    long_description_content_type='text/markdown',  # This is important to specify the markdown format
    author='Amir Jaber',
    packages=find_packages(),
    install_requires=[
        'pandas==2.1.3',
        'snowflake-connector-python==3.5.0',
        'pyarrow==14.0.1',
        'duckdb==0.9.2',
        'db-dtypes==1.2.0',
        'pyyaml==6.0.1',
        'google-cloud-bigquery==3.14.1'
    ],
    entry_points={
        'console_scripts': [
            'quack=quacker.cli:main',
        ],
    },
)