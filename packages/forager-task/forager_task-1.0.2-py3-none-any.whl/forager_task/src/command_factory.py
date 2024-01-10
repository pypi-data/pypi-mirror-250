"""
This script is used to determine which command will be run.

Author: Maksym Sydorchuk
Data: 8/01/2024
"""

from ..src.command_abstract import Command
from ..src.commands.delete_record_command import DeleteRecordCommand
from ..src.commands.domain_search_command import DomainSearch
from ..src.commands.email_verification_command import EmailVerification
from ..src.commands.get_record_command import GetRecordCommand
from ..src.services.storage_service_json import JSONSaveService
from ..src.services.storage_service_sqlite import SQLiteSaveService
from ..src.storage_service_abstract import StorageService


class SaveFactory(object):
    """
    A class SaveFactory.

    Method
    -------
    get_save_service:  Determine which type of storage service will be used.
    """

    def get_save_service(self, save_strategy: str) -> StorageService:
        """
        Determine which type of storage service will be used.

        :param save_strategy: Type of storage service ('to_db', 'to_file').

        :return:Type of storage service what will be used (SQLiteSaveService, JSONSaveService).
        """
        if save_strategy == 'to_db':
            return SQLiteSaveService()
        if save_strategy == 'to_file':
            return JSONSaveService()
        raise ValueError('No save_strategy was provided')


class CommandFactory(object):
    """
    A class Command.

    Method
    -------
    get_task: Determine which command will be executed and with what parameters.
    """

    def get_task(self, command: str, command_args: dict, storage_service: StorageService, api_key: str) -> Command:
        """
        Determine which command will be executed and with what parameters.

        :param command: Type of command.
        :param command_args: Parameters what needed for current command.
        :param storage_service: Type of storage service what will be used with current command.
        :param api_key: Your api key to use api service.
        :return:
        """
        if command == 'email_verification':
            return EmailVerification(command_args, storage_service, api_key)
        elif command == 'domain_search':
            return DomainSearch(command_args, storage_service, api_key)
        elif command == 'get_record':
            return GetRecordCommand(command_args, storage_service)
        elif command == 'delete_record':
            return DeleteRecordCommand(command_args, storage_service)
        raise ValueError('No command was provided')
