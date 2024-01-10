from abc import ABC, abstractmethod


class AbstractStorageClient(ABC):
    @abstractmethod
    def retrieve(self, **params):
        ...
        
    @abstractmethod
    def create(self, **params):
        ...
        
    @abstractmethod
    def update(self, **params):
        ...
        
    @abstractmethod
    def delete(self, **params):
        ...

    @abstractmethod
    def bulk_retrieve(self, **params):
        ...
        
    @abstractmethod
    def bulk_create(self, **params):
        ...
        
    @abstractmethod
    def bulk_update(self, **params):
        ...
        
    @abstractmethod
    def bulk_delete(self, **params):
        ...
