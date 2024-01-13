import requests
from requests.auth import HTTPBasicAuth
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.ssh_hook import SSHHook
from airflow.exceptions import AirflowException

class GeoNodeOperator(BaseOperator):
    template_fields = ('user', 'password', 'layers', 'style_xml', 'metadata_data', 'document_path', 'document_title', 'map_data', 'resource_id', 'permiss_data')

    @apply_defaults
    def __init__(self, user="", password="", map_data="", resource_id="", permiss_data="", base_url="", metadata_data="", layers="",style_xml = "", document_path="", document_title="", method="", style_name="", *args, **kwargs):
        super(GeoNodeOperator, self).__init__(*args, **kwargs)
        self.user = user
        self.password = password
        self.base_url = base_url
        self.metadata_data = metadata_data
        self.layers = layers
        self.permiss_data = permiss_data
        self.resource_id = resource_id
        self.map_data = map_data
        self.style_xml = style_xml
        self.document_path = document_path
        self.document_title = document_title
        self.method = method
        self.style_name = style_name

    def execute(self, context):
        if self.method == 'publish_layer':
            self.publish_layer()
        elif self.method == 'update_vector_layer':
            self.update_vector_layer()
        elif self.method == 'update_layer_style':
            self.update_layer_style()
        elif self.method == 'upload_document':
            self.upload_document()
        elif self.method == 'upload_map':
            self.upload_map()
        elif self.method == 'upload_metadata':
            self.upload_metadata()
        elif self.method == 'update_layer':
            self.update_layer()
        elif self.method == 'set_permiss':
            self.set_permiss()    
        # Agregar mas metodos de ser necesarios..

    def publish_layer(self, context):
        for layer_name in self.layers:
            login = HTTPBasicAuth(self.user, self.password)
            headers = {'Content-Type': 'application/xml'}
            url = f'{self.base_url}/geoserver/rest/workspaces/geonode/featuretypes'
            xml = f'<featureType><name>{layer_name}</name><enabled>false</enabled><srs>EPSG:3857</srs><projectionPolicy>FORCE_DECLARED</projectionPolicy></featureType>'
            r = requests.post(url=url, auth=login, data=xml, headers=headers, verify=False)

            if r.status_code == 201:
                print(f'Layer {layer_name} published successfully.')
            else:
                print(f'Error publishing layer {layer_name}. Status code: {r.status_code}')

    def update_vector_layer(self):
        # Implementar lógica
        pass

    def update_layer_style(self):   
        url = f"{self.base_url}/geoserver/rest/layers/geonode:{self.layers}"
        auth = (self.user, self.password)
        headers = {"Content-type": "text/xml"}
        data = f"<layer><defaultStyle><name>{self.style_name}</name></defaultStyle></layer>"

        response = requests.put(url, auth=auth, headers=headers, data=data)

        if response.status_code == 200:
            print(f"{self.layers} style updated successfully.")
        else:
            print(f"Failed to update {self.layers} style. Status code: {response.status_code}")

    def upload_document(self, context):
        auth = HTTPBasicAuth(self.user, self.password)
        url = f'{self.base_url}/api/v2/documents'
        payload = {'title': self.document_title}
        files = [('doc_file', (self.document_path, open(self.document_path, 'rb'), 'document/pdf'))]

        response = requests.post(url, auth=auth, data=payload, files=files)
        self.log.info(f'Document uploaded. Status code: {response.status_code}')


    def upload_map (self,context):

        map_create_url = f"{self.base_url}/api/v2/maps/"
        response = requests.post(map_create_url, json=self.map_data, auth=(self.user, self.password))
        print(response)

        if response.status_code == 201:
            map_id = response.json()['map']
            print(f"Map created successfully with ID: {map_id}")

    def upload_metadata (self):
        #Utilizar el layer id en vez del layer_name
        url = f"{self.base_url}/api/v2/datasets/{self.resource_id}"
        headers = {'Content-Type': 'application/json'}

        #esta request actualiza directamente en GEONODE los metadatos
        response = requests.patch(url, auth=(self.user, self.password), json=self.metadata_data, headers=headers)
        if response.status_code == 200:
            print('Patch successful!')
        else:
            print(f'Error: {response.status_code} - {response.text}')

    def update_layer(self):
        self.log.info("Executing update_layer operator")

        # Get the SSH hook
        #ssh_hook = BaseHook.get_hook(conn_id=self.ssh_conn_id)
        ssh = SSHHook(ssh_conn_id="ssh_demo4")
        ssh_client = None

        # Build the command to execute inside the Docker container
        command = f"docker exec django4geonode python manage.py updatelayers -f {self.layers}"

        try:
            # Execute the command via SSH
            ssh_client = ssh.get_conn()
            ssh_client.load_system_host_keys()
            ssh_client.exec_command(command)
            self.log.info("Layer update successful")
        except Exception as e:
            self.log.error(f"Error updating layer: {str(e)}")
            raise AirflowException("Layer update failed")

        self.log.info("Update_layer operator complete")

    def set_permiss(self):

        #Setear capa para que sea visible solo a Usuarios Registrados
 
        url = f"{self.base_url}/api/v2/resources/{self.resource_id}/permissions"



        response = requests.patch(url, auth=(self.user, self.password), json=self.permiss_data)
        print(response.status_code)


