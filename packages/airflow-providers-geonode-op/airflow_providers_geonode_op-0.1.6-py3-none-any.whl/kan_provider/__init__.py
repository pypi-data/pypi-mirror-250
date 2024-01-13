__version__ = "0.1.6"


def get_provider_info() -> dict:
    return {
        "package-name": "airflow_providers_geonode_op",
        "name": "Geonode Airflow Provider",
        "description": "Custom GeoNode provider for Apache Airflow",
        "versions": [__version__]
    }