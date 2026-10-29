#!/bin/env python3

from pathlib import Path

from sqlalchemy.engine import URL

from modules.utilities.utilities import utilities as util

class database_utils():
    '''
    This class functions as a collection of function to prepare a connection to a database.
    '''

    @staticmethod
    def generate_connection_string(database_config: dict) -> tuple[bool, str]:
        if "type" not in database_config:
            return False, ''

        match database_config['type']:
            case 'sqlite':
                local_database_path = Path("./database").resolve()
                if not util.ensure_directory(str(local_database_path)):
                    return False, ''
                connection_string = URL.create(
                    "sqlite",
                    database=str(local_database_path / "wgdashboard.db"),
                ).render_as_string(hide_password=False)

            case 'postgresql' | 'postgres':
                connection_string = URL.create(
                    "postgresql+psycopg",
                    username=database_config.get("username") or None,
                    password=database_config.get("password") or None,
                    host=database_config.get("host") or "localhost",
                    port=int(database_config.get("port") or 5432),
                ).render_as_string(hide_password=False)

            case 'mariadb':
                connection_string = URL.create(
                    "mariadb+mariadbconnector",
                    username=database_config.get("username") or None,
                    password=database_config.get("password") or None,
                    host=database_config.get("host") or "localhost",
                    port=int(database_config.get("port") or 3306),
                ).render_as_string(hide_password=False)

            case 'mysql':
                connection_string = URL.create(
                    "mysql+pymysql",
                    username=database_config.get("username") or None,
                    password=database_config.get("password") or None,
                    host=database_config.get("host") or "localhost",
                    port=int(database_config.get("port") or 3306),
                ).render_as_string(hide_password=False)

            case _:
                return False, ''

        return True, connection_string