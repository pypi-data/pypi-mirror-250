"""
This script is used to work with SQLite.

Author: Maksym Sydorchuk
Data: 8/01/2024
"""

import sqlite3

from ...src.storage_service_abstract import StorageService


class SQLiteSaveService(StorageService):
    """
    A class to implement CRUD operations with JSON.

    Attributes
    ----------
    db_name : str
        Name of your SQLite db in which will be saved information.

    Methods
    -------
     __init__: Create DB file, two tables "task_progress" and "email_status". Create connection and cursor.

    add_record: Insert current email information in your storage service.

    update_record: Update current email information in your storage service.

    get_record: Get current email information from your storage service.

    delete_record: Delete current email information from your storage service.

    """

    def __init__(self, db_name: str = 'forager.db') -> None:
        """
        Create DB file, two tables "task_progress" and "email_status". Create connection and cursor.

        :return: None
        """
        self.db_name = db_name
        try:
            self.query_create_db_table()
        except sqlite3.Error as error:
            print('DB connection error', error)
        except Exception as error:
            print(error, type(error))

    def __del__(self) -> None:
        """
        Close cursor and connection.

        :return: None
        """
        self.cursor.close()
        self.connection.close()

    def is_current_record_exist(self, data_args: dict) -> list:
        """
        Check if current email exist in storage.

        :param data_args: dict, response from email verification command.
        :return: bool
        """
        query = self.cursor.execute(
            'SELECT * FROM email_status WHERE email = ?',
            (data_args['email'],),
        )
        return query.fetchall()

    def add_record(self, data_args: dict) -> dict:
        """
        Insert email information in your storage service.

        :param data_args: dict, response from email verification command.
        :return: None
        """
        if self.is_current_record_exist(data_args):
            return self.update_record(data_args)
        else:
            try:
                return self.query_add_record(data_args)
            except sqlite3.Error as error:
                return {'status': error, 'data': None}
            except Exception as error:
                return {'status': error, 'data': None}

    def update_record(self, data_args: dict) -> dict:
        """
        Update current email information in your storage service.

        :param data_args: dict, response from email verification command.
        :return: None
        """
        try:
            return self.query_update_record(data_args)
        except sqlite3.Error as error:
            return {'status': 'Error', 'data': type(error)}
        except Exception as error:
            return {'status': 'Error', 'data': type(error)}

    def get_record(self, email: str) -> dict:
        """
        Get current email information from your storage service.

        :param email: str
        :return: None
        """
        try:
            return self.query_get_record(email)
        except sqlite3.Error as error:
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
            return self.query_record_delete(email)
        except sqlite3.Error as error:
            return {'status': 'Error', 'data': type(error)}
        except Exception as error:
            return {'status': 'Error', 'data': type(error)}

    def query_record_delete(self, email: str) -> dict:
        """
        Query to delete record from your storage service.

        :param email: str

        :return: dict
        """
        self.cursor.execute('DELETE FROM email_status WHERE email = ?', (email,))
        self.connection.commit()
        return {'status': 'Data deleted', 'data': None}

    def query_get_record(self, email: str) -> dict:
        """
        Query to get record from your storage service.

        :param email: str

        :return: dict
        """
        self.cursor.execute('SELECT * FROM email_status WHERE email = ?', (email,))
        emails = self.cursor.fetchone()
        if emails:
            self.connection.commit()
            return {'status': 'Success', 'data': emails}
        return {'status': 'No such data found', 'data': None}

    def query_update_record(self, data_args: dict) -> dict:
        """
        Query to update record to your storage service.

        :param data_args: dict

        :return:dict
        """
        self.cursor.execute(
            'UPDATE email_status SET status = ? WHERE email = ?',
            (data_args['email'], data_args['status']),
        )
        self.connection.commit()
        return {'status': 'Data updated', 'data': None}

    def query_add_record(self, data_args: dict) -> dict:
        """
        Query to add record to your storage service.

        :param data_args: dict

        :return:dict
        """
        self.cursor.execute(
            'INSERT INTO email_status (email, status) VALUES (?, ?)',
            (data_args['email'], data_args['status']),
        )
        self.connection.commit()
        return {'status': 'New data added', 'data': None}

    def query_create_db_table(self) -> None:
        """
        Query to create connection, db and table.

        :return: None
        """
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS email_status (
                        id INTEGER PRIMARY KEY,
                        email TEXT NOT NULL,
                        status TEXT NOT NULL
                        )
                        """)
        self.connection.commit()
