import pytest
from blob_downloader.settings import S
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError


@pytest.fixture
def setup_azurite(monkeypatch):
    "Fixture used to setup the connection to the Azure blob storage emulator"
    monkeypatch.setattr(S, "AZURE_BLOB_CONNECTION_STRING", "AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;DefaultEndpointsProtocol=http;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;")
    bsc = BlobServiceClient.from_connection_string(S.AZURE_BLOB_CONNECTION_STRING)
    try:
        bsc.get_container_client("test").create_container()
    except ResourceExistsError:
        pass
    