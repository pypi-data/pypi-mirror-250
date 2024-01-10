import logging

from src.storage.abstract import AbstractStorageClient


from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class DynamodbSettings(BaseSettings):
    table: str


class DynamodbStorageClient(AbstractStorageClient):
    def __init__(self, settings: DynamodbSettings):
        ...
        
    def __call__(self):
        logger.info("Hello world")
