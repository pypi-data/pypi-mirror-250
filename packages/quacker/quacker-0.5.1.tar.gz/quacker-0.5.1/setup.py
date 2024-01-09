from setuptools import setup, find_packages

setup(
    name='quacker',
    version='0.5.1',
    description='Sync dbt sources and models from cloud warehouses to duckdb',
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
