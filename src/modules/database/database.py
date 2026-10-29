#!/bin/env python3

import logging as log

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.exc import SQLAlchemyError

from .schema import Base
from .database_utils import database_utils

class database():
    @staticmethod
    def create_session(database_config: dict) -> tuple[bool, sqlalchemy.engine.Engine | None, sqlalchemy.orm.Session | None]:
        ok, connection_string = database_utils.generate_connection_string(database_config)
        if not ok:
            log.error("failed to generate the connection string")
            return False, None, None

        try:
            engine = sqlalchemy.create_engine(connection_string, echo=False)

            local_session = sqlalchemy.orm.sessionmaker(bind=engine)
            session = local_session()

            return True, engine, session

        except Exception as err:
            log.critical(f'database initialization failed: {err}')
            return False, None, None
    
    @staticmethod
    def ensure_contents(engine) -> bool:
        try:
            log.info('checking if all tables are present, and creating them if they are not')

            Base.metadata.create_all(engine)

            return True

        except SQLAlchemyError:
            log.exception('failed to verify contents of the database')
            return False
