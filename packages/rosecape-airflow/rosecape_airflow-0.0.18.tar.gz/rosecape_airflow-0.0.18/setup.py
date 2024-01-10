from setuptools import setup, find_packages

VERSION = '0.0.18'
DESCRIPTION = 'Airflow utilities'
LONG_DESCRIPTION = 'A package that makes it easy to interact with AWS services from Airflow using PythonOperator'

setup(
    name="rosecape_airflow",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Nick Joanis",
    author_email="nicholas@rosecape.ca",
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'boto3==1.26.142'
    ],
    keywords='Airflow',
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)
