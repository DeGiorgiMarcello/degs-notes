from blob_downloader.drivers.azure_blob import AzureBlobStorage
from unittest.mock import Mock, create_autospec
from azure.storage.blob import ContainerClient
from blob_downloader.settings import S
import pytest
from pathlib import Path


@pytest.fixture
def mocked_container_client(monkeypatch):
    mock_container = create_autospec(ContainerClient)
    monkeypatch.setattr("blob_downloader.drivers.azure_blob.ContainerClient", mock_container)
    return mock_container

def test_azure_blob_storage(mocked_container_client):
    AzureBlobStorage(conn_str="foo", container="bar")
    mocked_container_client.from_connection_string.assert_called_with(conn_str="foo",container_name="bar")

def test_azure_blob_storage_from_settings(monkeypatch, mocked_container_client):
    monkeypatch.setattr(S, "AZURE_BLOB_CONNECTION_STRING", "mock_connection_str")
    monkeypatch.setattr(S, "AZURE_CONTAINER", "mock_container")

    AzureBlobStorage()
    mocked_container_client.from_connection_string.assert_called_with(
        conn_str=S.AZURE_BLOB_CONNECTION_STRING,
        container_name=S.AZURE_CONTAINER
        )
    
def test_azure_blob_storage_no_args_nor_default(monkeypatch):
    monkeypatch.setattr(S, "AZURE_BLOB_CONNECTION_STRING", None)
    monkeypatch.setattr(S, "AZURE_CONTAINER", None)
    with pytest.raises(ValueError, match="Both connection string and container are mandatory."):
        AzureBlobStorage()

def test_azure_blob_pull_push_same_name(setup_azurite, tmp_path, monkeypatch):
    output_folder = tmp_path / "output"
    monkeypatch.setattr(S, "OUTPUT_FOLDER", output_folder)
    driver = AzureBlobStorage(container="test")

    src_uri = (tmp_path / "test.txt")
    src_uri.write_text("This is a test file :)")

    driver.push(src_uri=str(src_uri))

    dst_path = (output_folder / "test.txt")
    assert not dst_path.exists()
    driver.pull("test.txt")
    assert dst_path.exists()



