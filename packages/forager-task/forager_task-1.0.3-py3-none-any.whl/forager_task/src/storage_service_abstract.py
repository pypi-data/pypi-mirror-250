"""
This script is used to abstract class StorageService.

Author: Maksym Sydorchuk
Data: 8/01/2024
"""

from abc import ABC, abstractmethod


class StorageService(ABC):
    """
    An abstract class StorageService.

    Methods
    -------
    add_record: Abstract method to add the record in your storage.
    update_record: Abstract method to update the record in your storage.
    get_record: Abstract method to get the record from your storage.
    delete_record: Abstract method to delete the record in your storage.
    """

    @abstractmethod
    def add_record(self, data_args: dict) -> dict:
        """
        Abstract method to add the record in your storage.

        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def update_record(self, data_args: dict) -> dict:
        """
        Abstract method to update the record in your storage.

        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def get_record(self, email: str) -> dict:
        """
        Abstract method to get the record from your storage.

        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def delete_record(self, email: str) -> dict:
        """
        Abstract method to delete the record in your storage.

        :return:
        """
        raise NotImplementedError
