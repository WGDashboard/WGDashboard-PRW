#!/bin/env python3

from datetime import datetime
import sqlalchemy.orm

import json

from .schema import Base
from .schema import Apikeys

class functions():
    def retrieve_api_keys(session: sqlalchemy.orm.Session) -> tuple[list[dict], list[dict]]:
        """ AI GENERATED
        Retrieve all API keys from the database and separate them into valid and expired keys.

        Parameters
        ----------
        session : sqlalchemy.orm.Session
            An active SQLAlchemy session connected to the database.

        Returns
        -------
        tuple[list[dict], list[dict]]
            A tuple containing two lists of dictionaries:
            - The first list contains valid API keys (not expired at the time of the call).
            - The second list contains expired API keys (already expired at the time of the call).

            Each dictionary has the following keys:
            - 'id': int, the primary key of the API key record
            - 'key': str, the API key string
            - 'creation': str, timestamp of when the key was created
            - 'expiration': str or None, timestamp of when the key expires, or None if no expiration

        Notes
        -----
        - Keys with no expiration date are considered valid.
        - Expiration comparison is performed against the current system time.
        """

        time_now = datetime.now()
        stored_keys = session.query(Apikeys).all()

        expired_keys = []
        valid_keys = []

        for key in stored_keys:
            expiration_date = None

            if key.key_expiration:
                expiration_date = datetime.strptime(key.key_expiration, "%Y-%m-%d %H:%M:%S")

            key_dict = key.to_dict()

            if expiration_date is None or expiration_date > time_now:
                valid_keys.append(key_dict)
            else:
                expired_keys.append(key_dict)
        
        print("VALID:", json.dumps(valid_keys,indent=4))
        print("INVALID", json.dumps(expired_keys, indent=4))

        return valid_keys, expired_keys