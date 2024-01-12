from setuptools import setup, find_packages

setup(
    name='airflow-providers-geonode-op',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'requests',  # Add any dependencies your operator requires
        #'apache-airflow',  # Ensure Apache Airflow is listed as a dependency
    ],
    entry_points={
        'apache_airflow_provider': [
            'airflow_providers_geonode_op = airflow_providers_geonode_op.geonode_operator_module:get_provider_info',
        ],
    },
    author='Kan territory & IT',
    author_email='develop@kan-gl.com',
    description='Custom GeoNode Operator for Apache Airflow',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)