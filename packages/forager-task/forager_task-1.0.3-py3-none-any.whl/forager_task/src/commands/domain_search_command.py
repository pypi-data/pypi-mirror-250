"""
This script is used to execute domain search command.

Author: Maksym Sydorchuk
Data: 8/01/2024
"""

import re

from ...src.api_services.hunter_api_service import HunterApiService
from ...src.command_abstract import Command
from ...src.storage_service_abstract import StorageService


class DomainSearch(Command):
    """
    A class to represent a domain search command.

    Attributes
    ----------
    domain : str
        The domain you want to find information about.
    command_name : str
        Command name.

    Methods
    -------
    __init__:
    Create a DomainSearch command.

    validate_command_argument:
    Check that a domain is provided in the command argument.

    execute:
    Execute current command.
    """

    domain: str
    api_key: str
    command_name = 'domain_search'

    def __init__(self, command_args: dict, storage_service: StorageService, api_key: str) -> None:
        """
        Create a DomainSearch command.

        :param command_args: dict with key 'domain' - {'domain': 'YOUR_DOMAIN'}
        :param storage_service: StorageService type
        """
        super().__init__(command_args, storage_service)
        self.domain = command_args['domain']
        self.api_key = api_key

    def validate_command_argument(self) -> None:
        """
        Check that a domain is provided in the command argument.

        :return:

        Causes an exception if no domain was specified.
        """
        if not self.command_args.get('domain'):
            raise ValueError('No email was provided')
        if not re.fullmatch(r'^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,}$', self.command_args['domain']):
            raise ValueError('Invalid domain name')

    def execute(self) -> dict:
        """
        Execute current command.

        :return:

        Return all the email addresses found using one given domain name, with sources.
        """
        response = HunterApiService().domain_search(self.domain, self.api_key)
        return {'command': self.command_name, 'status': 'success', 'data': response}
