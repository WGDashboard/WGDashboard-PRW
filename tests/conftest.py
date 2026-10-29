from collections.abc import Callable, Iterator
from copy import deepcopy
from pathlib import Path
from typing import Any

import bcrypt
import flask
import pytest
from flask.testing import FlaskClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from main import create_app
from modules.database.schema import Base


DEFAULT_CONFIG: dict[str, Any] = {
    "server": {
        "authentication_required": True,
        "wgdashboard_apikey": False,
        "log_level": "ERROR",
        "app_prefix": "",
        "version": "1.0.0",
    },
    "account": {
        "username": "admin",
        "password": bcrypt.hashpw(b"correct horse", bcrypt.gensalt()).decode("utf-8"),
        "enable_totp": False,
        "totp_verified": False,
        "totp_key": "JBSWY3DPEHPK3PXP",
    },
    "other": {"welcome_session": False},
    "database": {"type": "sqlite"},
}


@pytest.fixture
def memory_engine() -> Iterator[Engine]:
    '''Provide an isolated in-memory SQLite engine.'''
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def app_factory(
    memory_engine: Engine,
    tmp_path: Path,
) -> Callable[[dict[str, Any] | None], flask.Flask]:
    '''Create apps from configurable defaults using the in-memory database.'''
    def factory(overrides: dict[str, Any] | None = None) -> flask.Flask:
        config_data = deepcopy(DEFAULT_CONFIG)
        if overrides is not None:
            for section, values in overrides.items():
                config_data.setdefault(section, {}).update(values)

        application = create_app(
            config_data,
            database_engine=memory_engine,
            secret_key_path=tmp_path / "secret_key",
        )
        application.config["TESTING"] = True
        return application

    return factory


@pytest.fixture
def app(app_factory: Callable[[dict[str, Any] | None], flask.Flask]) -> flask.Flask:
    '''Provide a configured Flask app for route tests.'''
    return app_factory(None)


@pytest.fixture
def client(app: flask.Flask) -> FlaskClient:
    '''Provide the test client for the Flask app.'''
    return app.test_client()
