"""
This script is used to work with JSON file.

Author: Maksym Sydorchuk
Data: 8/01/2024
"""

import json

from ...src.storage_service_abstract import StorageService


class JSONSaveService(StorageService):
    """
    A class to implement CRUD operations with JSON.

    Attributes
    ----------
    file_name : str
        Name of your JSON file in which will be saved information.

    Methods
    -------
    add_record:
    Insert or update current email information in your storage service.

    update_record:
    This method realized in add_record.

    get_record:
    Get current email information from your storage service.

    delete_record:
    Delete current email information from your storage service.
    """

    file_name = 'email_verification.json'

    def add_record(self, data_args: dict) -> dict:
        """
        Insert or update current email information in your storage service.

        :param data_args: dict, response from email verification command.
        :return: None
        """
        try:
            with open(self.file_name, encoding='utf8') as file_email_verification:
                data_from_file = json.load(file_email_verification)
                for item_from_file in data_from_file:
                    if item_from_file['email'] == data_args['email']:
                        return self.update_record(data_args)
                data_from_file.append({'email': data_args['email'], 'data': data_args})
                with open(self.file_name, 'w', encoding='utf8') as outfile:
                    json.dump(data_from_file, outfile, indent=4, ensure_ascii=False)
                    return {'status': 'New data added', 'data': None}
        except FileNotFoundError:
            with open(self.file_name, 'w', encoding='utf8') as new_file:
                json.dump(
                    [{'email': data_args['email'], 'data': data_args}],
                    new_file,
                    indent=4,
                    ensure_ascii=False,
                )
            return {'status': 'File created', 'data': None}
        except Exception as error:
            return {'status': 'Error', 'data': type(error)}

    def update_record(self, data_args: dict) -> dict:
        """
        Realized in add_record.

        :param data_args: dict

        :return: dict
        """
        with open(self.file_name, encoding='utf8') as file_email_verification:
            data_from_f = json.load(file_email_verification)
            for item_from_file in data_from_f:
                if item_from_file['email'] == data_args['email']:
                    data_from_f[data_from_f.index(item_from_file)] = {'email': data_args['email'], 'data': data_args}
            with open(self.file_name, 'w', encoding='utf8') as outfile:
                json.dump(data_from_f, outfile, indent=4, ensure_ascii=False)
                return {'status': 'File updated', 'data': None}

    def get_record(self, email: str) -> dict:
        """
        Get current email information from your storage service.

        :param email: str
        :return: dict
        """
        try:
            with open(self.file_name, encoding='utf8') as file_email_verification:
                data_from_file = json.load(file_email_verification)
                for file_item in data_from_file:
                    if file_item['email'] == email:
                        return {'status': 'Success', 'data': file_item}
                return {'status': 'No such data found', 'data': None}
        except FileNotFoundError as error:
            return {'status': 'Error', 'data': type(error)}
        except Exception as error:
            return {'status': 'Error', 'data': type(error)}

    def delete_record(self, email: str) -> dict:
        """
        Delete current email information from your storage service.

        :param email: str
        :return: None
        """
        try:
            with open(self.file_name, encoding='utf8') as file_email_verification:
                data_from_f = json.load(file_email_verification)
                for item_from_file in data_from_f:
                    if item_from_file['email'] == email:
                        data_from_f.remove(item_from_file)
                with open(self.file_name, 'w', encoding='utf8') as outfile:
                    json.dump(data_from_f, outfile, indent=4, ensure_ascii=False)
                    return {'status': 'Data deleted', 'data': None}
        except FileNotFoundError as error:
            return {'status': 'Error', 'data': type(error)}
        except Exception as error:
            return {'status': 'Error', 'data': type(error)}
