"""
This script is used to execute delete command.

Author: Maksym Sydorchuk
Data: 8/01/2024
"""

import re

from ...src.command_abstract import Command
from ...src.storage_service_abstract import StorageService


class DeleteRecordCommand(Command):
    """
    A class to represent a delete record command.

    Attributes
    ----------
    email : str
        The email what you want to delete from your storage.
    command_name : str
        Command name.

    Methods
    -------
    __init__:
    Create a DeleteRecordCommand.

    validate_command_argument:
    Check that an email address is provided in the command argument.

    execute:
    Execute current command and delete email from your storage.
    """

    email: str
    command_name = 'delete_record'

    def __init__(self, command_args: dict, storage_service: StorageService) -> None:
        """
        Create a DeleteRecordCommand.

        :param command_args: dict with key 'email' - {'email': 'YOUR_EMAIL'}
        :param storage_service: StorageService type
        """
        super().__init__(command_args, storage_service)
        self.email = command_args['email']

    def validate_command_argument(self) -> None:
        """
        Check that an email address is provided in the command argument.

        :return:

        Causes an exception if no email was specified.
        """
        if not self.command_args.get('email'):
            raise TypeError('No email was provided')
        if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', self.command_args['email']):
            raise ValueError('Invalid email address')

    def execute(self) -> dict:
        """
        Execute current command and delete email from your storage.

        :return:

        Return the dict with the status of execution.
        """
        response = self.storage_service.delete_record(self.email)
        return {'command': self.command_name, 'status': response['status'], 'data': response['data']}
