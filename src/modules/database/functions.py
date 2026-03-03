#!/bin/env python3

from datetime import datetime
import sqlalchemy.orm

from .schema import Base
from .schema import Apikeys

class functions():
    def retrieve_api_keys(session: sqlalchemy.orm.Session) -> dict:
        time_now = datetime.now()

        api_keys = session.query(Apikeys).all()
        print(dict(api_keys))

        return {}