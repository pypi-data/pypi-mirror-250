from abc import ABC, abstractmethod


class AbstractStorageClient(ABC):
    @abstractmethod
    def retrieve(self, **kwargs):
        ...

    @abstractmethod
    def create(self, **kwargs):
        ...

    @abstractmethod
    def update(self, **kwargs):
        ...

    @abstractmethod
    def delete(self, **kwargs):
        ...

    @abstractmethod
    def bulk_retrieve(self, **kwargs):
        ...

    @abstractmethod
    def bulk_create(self, **kwargs):
        ...

    @abstractmethod
    def bulk_update(self, **kwargs):
        ...

    @abstractmethod
    def bulk_delete(self, **kwargs):
        ...
