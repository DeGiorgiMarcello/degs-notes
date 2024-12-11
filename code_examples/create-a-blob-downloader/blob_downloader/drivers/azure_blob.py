from blob_downloader.drivers.i_driver import Driver
from azure.storage.blob import ContainerClient
from blob_downloader.settings import S
from pathlib import Path


class AzureBlobStorage(Driver):
    def __init__(
        self,
        conn_str: str = S.AZURE_BLOB_CONNECTION_STRING,
        container: str = S.AZURE_CONTAINER,
    ):
        if not conn_str or container:
            raise ValueError("Both connection string and container are mandatory.")

        self.container_client = ContainerClient.from_connection_string(
            conn_str, container
        )

    def pull(self, blob_uri: str):
        blob_client = self.container_client.get_blob_client(blob_uri)
        blob = blob_client.download_blob()
        dst_path = Path(S.OUTPUT_FOLDER) / blob.name
        dst_path.mkdir(parents=True, exist_ok=True)

        with open(dst_path, "w") as f:
            f.write(blob)

    def push(self, src_uri: str, dst_uri):
        blob_client = self.container_client.get_blob_client(src_uri)

        with open(src_uri, "rb") as f:
            blob_client.upload_blob(f)

    def list_blobs(self, folder: str = None):
        names = self.container_client.list_blob_names()

        if folder:
            names = [n for n in names if folder in n]
        return names
