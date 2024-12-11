from blob_downloader.drivers.i_driver import Driver
from azure.storage.blob import ContainerClient
from blob_downloader.settings import S
from pathlib import Path


class AzureBlobStorage(Driver):
    def __init__(
        self,
        conn_str: str = None,
        container: str = None,
    ):
        # default values not used for problems in tests with monkeypatch and singletons 
        conn_str = conn_str if conn_str else S.AZURE_BLOB_CONNECTION_STRING
        container = container if container else S.AZURE_CONTAINER

        if not conn_str or not container:
            raise ValueError("Both connection string and container are mandatory.")

        self.container_client = ContainerClient.from_connection_string(
            conn_str, container
        )

    def pull(self, blob_uri: str):
        blob_client = self.container_client.get_blob_client(blob_uri)
        blob = blob_client.download_blob()
        dst_path = Path(S.OUTPUT_FOLDER) / blob.name
        dst_path.parent.mkdir(parents=True, exist_ok=True)

        with open(dst_path, "wb") as f:
            f.write(blob.readall())

    def push(self, src_uri: str, dst_uri: str | None = None):
        if not dst_uri:
            dst_uri = Path(src_uri).name

        blob_client = self.container_client.get_blob_client(dst_uri)

        with open(src_uri, "rb") as f:
            blob_client.upload_blob(f, overwrite=True)

    def list_blobs(self, folder: str = None):
        names = self.container_client.list_blob_names()

        if folder:
            names = [n for n in names if folder in n]
        return names
