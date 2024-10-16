from azure.storage.blob import ContainerClient
from settings import S


def get_container_client(container_name: str) -> ContainerClient:
    """
    Get the container client from the connection string and the container name

    Returns:
        ContainerClient: the container client
    """
    from azure.storage.blob import ContainerClient

    return ContainerClient.from_connection_string(
        S.CONNECTION_STRING.get_secret_value(),
        container_name=container_name,
        connection_timeout=300,
        read_timeout=300,
    )


def download_blobs(container_name: str, starts_with: str = ""):
    container_client = get_container_client(container_name)
    for blob in container_client.list_blobs(name_starts_with=starts_with):
        blob_client = container_client.get_blob_client(blob.name)
        file_dst = S.OUTPUT_FOLDER / blob.name

        if not file_dst.parent.exists():
            file_dst.parent.mkdir(parents=True)

        with open(file_dst, "wb") as f:
            data = blob_client.download_blob().readall()
            f.write(data)


if __name__ == "__main__":
    download_blobs()
