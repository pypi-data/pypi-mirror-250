"""
This script is used to execute email verification command.

Author: Maksym Sydorchuk
Data: 8/01/2024
"""

import re

from ...src.api_services.hunter_api_service import HunterApiService
from ...src.command_abstract import Command
from ...src.storage_service_abstract import StorageService


class EmailVerification(Command):
    """
    A class to represent a email verification command.

    Attributes
    ----------
    email : str
        The email you want to verify.
    command_name : str
        Command name.

    Methods
    -------
    __init__:
    Create a EmailVerification command.

    validate_command_argument:
    Check that an email is provided in the command argument.

    execute:
    Execute current command.
    """

    email: str
    api_key: str
    command_name = 'email_verification'

    def __init__(self, command_args: dict, storage_service: StorageService, api_key: str) -> None:
        """
        Create a EmailVerification command.

        :param command_args: dict with key 'email' - {'email': 'YOUR_EMAIL'}
        :param storage_service: StorageService type
        """
        super().__init__(command_args, storage_service)
        self.email = command_args['email']
        self.api_key = api_key

    def validate_command_argument(self) -> None:
        """
        Check that an email is provided in the command argument.

        :return:

        Causes an exception if no email was specified.
        """
        if not self.command_args.get('email'):
            raise ValueError('No email was provided')
        if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', self.command_args['email']):
            raise ValueError('Invalid email address')

    def execute(self) -> dict:
        """
        Execute current command.

        :return:

        Saved response in your storage, what was defined in the save_strategy and return the status of your request.
        """
        response_from_api = HunterApiService().email_verify(self.email, self.api_key)
        response = self.storage_service.add_record(response_from_api)
        return {'command': self.command_name, 'status': response['status'], 'data': response['data']}
