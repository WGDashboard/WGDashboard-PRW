#!/bin/env python3

import os
import secrets
from pathlib import Path
from typing import Any

import flask
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from modules.config.config import config
from modules.config.config_utils import config_utils
from modules.config.legacy_keys import normalize_config_keys
from modules.database.database import database
from modules.routes.routes_general import routes_general
from modules.routes.routes_welcome import routes_welcome
from modules.utilities.logger import setup_logger


def _read_persistent_secret(secret_path: Path) -> str:
    '''Read the persistent session key, creating it once when needed.'''
    secret_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        descriptor = os.open(
            secret_path,
            os.O_CREAT | os.O_EXCL | os.O_WRONLY,
            0o600,
        )
    except FileExistsError:
        secret_key = secret_path.read_text(encoding="utf-8").strip()
        if not secret_key:
            raise RuntimeError(f"persistent secret key is empty: {secret_path}")
        return secret_key

    secret_key = secrets.token_urlsafe(64)
    with os.fdopen(descriptor, "w", encoding="utf-8") as secret_file:
        secret_file.write(secret_key)
        secret_file.flush()
        os.fsync(secret_file.fileno())

    return secret_key


def create_app(
    config_data: dict[str, Any] | None = None,
    *,
    database_url: str | None = None,
    database_engine: Engine | None = None,
    secret_key_path: str | Path | None = None,
) -> flask.Flask:
    '''Create and configure the WGDashboard Flask application.'''
    config_file_path: str | None = None
    if config_data is None:
        config_loaded, loaded_config = config.read()
        if not config_loaded:
            raise RuntimeError("failed to read the WGDashboard configuration")
        config_data = loaded_config

        config_path_found, config_file_path = config_utils.search_known_paths()
        if not config_path_found:
            raise RuntimeError("failed to locate the WGDashboard configuration")

    normalized_config = normalize_config_keys(config_data)
    server_config_found, server_config = config.filter(normalized_config, "SERVER")
    if not server_config_found:
        raise RuntimeError("the SERVER configuration section is missing")

    setup_logger(str(server_config.get("log_level", "DEBUG")).upper())

    prefix_value = server_config.get("app_prefix", "")
    prefix = str(prefix_value).rstrip("/")
    if prefix == "/":
        prefix = ""

    web_directory = Path(__file__).parent / "web" / "dist" / "WGDashboardAdmin"
    app = flask.Flask(
        "WGDashboard",
        static_url_path=f"{prefix}/web",
        template_folder=str(web_directory),
        static_folder=str(web_directory),
    )
    app.config["APP_PREFIX"] = prefix
    app.config["WGD_CONFIG"] = normalized_config
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    if secret_key_path is None:
        if config_file_path is not None:
            secret_path = Path(config_file_path).resolve().parent / "secret_key"
        else:
            secret_path = Path.home() / ".config" / "wgdashboard" / "secret_key"
    else:
        secret_path = Path(secret_key_path)
    app.secret_key = _read_persistent_secret(secret_path)

    database_config_found, database_config = config.filter(normalized_config, "DATABASE")
    if (
        not database_config_found
        and database_url is None
        and database_engine is None
    ):
        raise RuntimeError("the DATABASE configuration section is missing")

    if database_url is not None and database_engine is not None:
        raise ValueError("provide either database_url or database_engine, not both")

    if database_engine is not None:
        engine = database_engine
        db_session = sessionmaker(bind=engine, class_=Session)()
    elif database_url is None:
        session_created, engine, db_session = database.create_session(database_config)
        if not session_created or engine is None or db_session is None:
            raise RuntimeError("failed to initialize the database")
    else:
        engine = create_engine(database_url)
        db_session = sessionmaker(bind=engine, class_=Session)()

    if not database.ensure_contents(engine):
        engine.dispose()
        raise RuntimeError("failed to create or verify database tables")

    app.extensions["wgd_engine"] = engine
    app.extensions["wgd_db_session"] = db_session
    app.config["WGD_LOCALE_PATH"] = str(Path(__file__).parent / "web" / "locales")
    app.register_blueprint(routes_general, url_prefix=prefix)
    app.register_blueprint(routes_welcome, url_prefix=prefix)
    return app


if __name__ == "__main__":
    application = create_app()
    server_settings = application.config["WGD_CONFIG"]["server"]
    application.run(
        debug=server_settings.get("debug_enabled", False),
        host=server_settings.get("hostname", "0.0.0.0"),
        port=int(server_settings.get("port", 10086)),
        use_reloader=False,
    )
