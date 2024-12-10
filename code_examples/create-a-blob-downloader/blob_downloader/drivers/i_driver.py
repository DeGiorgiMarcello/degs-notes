from abc import ABC, abstractmethod

class Driver(meta=ABC):

    @abstractmethod
    def pull(self, blob_uri: str): ...

    @abstractmethod
    def push(self, src_uri: str, dst_uri: str): ...

    @abstractmethod
    def list_blobs(self, folder: str): ...