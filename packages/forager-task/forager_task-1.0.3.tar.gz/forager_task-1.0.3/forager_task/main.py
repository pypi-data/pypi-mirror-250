"""
This script is used to take command, arguments of this command, type of storage the data and return the result.

Author: Maksym Sydorchuk
Data: 8/01/2024
"""

from .src.command_factory import CommandFactory, SaveFactory


def handle_command(command: str, command_args: dict, save_strategy: str, api_key: str) -> dict:
    """
    Take command, arguments of this command, type of storage the data and return the result.

    :param command:
        'email_verification' - check the deliverability of a given email address, verifies if it has been found
        in https://hunter.io database, and saved it in your source, what was defined in the save_strategy.

        'domain_search' - return all the email addresses found using one given domain name, with sources.

        'get_record' - return the record from your source, what was defined in the save_strategy
        for current email.

        'delete_record' - delete the record from your source, what was defined in the save_strategy for current email.

    :param command_args:
        '{'email': 'YOUR_EMAIL'}' - used for commands 'email_verification', 'get_record', 'delete_record'.

        {'domain': 'YOUR_DOMAIN'} - used for command 'domain_search'

    :param save_strategy:
        'to_db' - SQLite is used for data storage

        'to_file' - JSON is used for data storage

    :param api_key:
        'API_KEY' - Your api key to use api service https://hunter.io

    :return:
        - 'email_verification' - saved response in your source, what was defined in the save_strategy
        - 'domain_search' - return dict
        - 'get_record' - return dict
        - 'delete_record' - return None

    """
    storage_service = SaveFactory().get_save_service(save_strategy)
    task = CommandFactory().get_task(command, command_args, storage_service, api_key)
    return task.execute()

