from setuptools import setup, find_packages

setup(
    name='airflow_providers_geonode_op',
    version='0.1.6',
    author='Kan Territory & IT',
    author_email='develop@kan-gl.com',
    description='Custom GeoNode Operator for Apache Airflow',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    install_requires=[
        'requests',
        'apache-airflow',
    ],
)