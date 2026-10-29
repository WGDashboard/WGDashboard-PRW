import runpy
from collections.abc import Callable
import logging
from pathlib import Path
from typing import Any
from urllib.error import URLError

import flask
import pyotp
import pytest
from flask.testing import FlaskClient
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect

from main import create_app
from modules.config.legacy_keys import normalize_config_keys
from modules.database.schema import Amnezia, Peers, Wireguard
from modules.routes.routes_general import white_list
from modules.utilities.utilities import utilities


def test_login_without_totp_has_correct_response_envelope(
    client: FlaskClient,
) -> None:
    response = client.post(
        "/api/authenticate",
        json={"username": "admin", "password": "correct horse"},
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "status": True,
        "message": "Login successful",
        "data": {"welcome_session": False},
    }
    assert "authToken=" in response.headers["Set-Cookie"]


def test_totp_login_verifies_submitted_code(
    app_factory: Callable[[dict[str, Any] | None], flask.Flask],
) -> None:
    application = app_factory({"account": {"enable_totp": True}})
    client = application.test_client()
    totp_code = pyotp.TOTP("JBSWY3DPEHPK3PXP").now()

    response = client.post(
        "/api/authenticate",
        json={
            "username": "admin",
            "password": "correct horse",
            "totp": totp_code,
        },
    )

    assert response.status_code == 200
    assert response.get_json()["status"] is True


def test_failed_login_returns_one_normalized_error_response(
    client: FlaskClient,
) -> None:
    response = client.post(
        "/api/authenticate",
        json={"username": "admin", "password": "wrong password"},
    )

    assert response.status_code == 401
    assert response.get_json() == {
        "status": False,
        "message": "Invalid username or password.",
        "data": {"status": False},
    }


def test_root_whitelist_does_not_allow_unlisted_api_routes(
    client: FlaskClient,
) -> None:
    response = client.get("/api/systemStatus")

    assert response.status_code == 401


def test_every_public_whitelist_path_is_registered(
    app: flask.Flask,
    client: FlaskClient,
) -> None:
    registered_rules = {rule.rule for rule in app.url_map.iter_rules()}

    for public_path in white_list:
        if public_path == "/web/":
            assert "/web/<path:filename>" in registered_rules
        else:
            assert public_path in registered_rules
    assert client.get("/api/getDashboardTheme").status_code == 200
    assert client.get("/api/locale").status_code == 200


def test_legacy_config_keys_are_normalized_with_canonical_precedence() -> None:
    normalized = normalize_config_keys(
        {
            "SERVER": {
                "auth_req": False,
                "authentication_required": True,
                "dashboard_api_key": True,
                "app_ip": "127.0.0.1",
                "app_port": "19000",
            }
        }
    )

    assert normalized == {
        "server": {
            "authentication_required": True,
            "wgdashboard_apikey": True,
            "hostname": "127.0.0.1",
            "port": "19000",
        }
    }


def test_interface_models_include_postdown_and_peer_fields() -> None:
    assert "iface_postdown" in Wireguard.__table__.columns
    assert "iface_postdown" in Amnezia.__table__.columns
    assert len(Peers.__table__.columns) > 2
    assert "peer_public_key" in Peers.__table__.columns


def test_secret_key_persists_across_factory_restarts(
    app_factory: Callable[[dict[str, Any] | None], flask.Flask],
    tmp_path: Path,
) -> None:
    first_app = app_factory(None)
    first_secret = first_app.secret_key
    second_app = create_app(
        first_app.config["WGD_CONFIG"],
        database_url="sqlite:///:memory:",
        secret_key_path=tmp_path / "secret_key",
    )

    assert second_app.secret_key == first_secret
    assert (tmp_path / "secret_key").stat().st_mode & 0o777 == 0o600


def test_gunicorn_factory_accepts_docker_ini_names(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    password_hash = (
        "$2b$12$1VN62Q7CS/BJcAahHAWsA.3CD6zPqWTmE/HN/AJqwP0zds2l25Fqe"
    )
    (tmp_path / "wg-dashboard.ini").write_text(
        "[Server]\n"
        "app_ip = 127.0.0.1\n"
        "app_port = 19000\n"
        "auth_req = true\n"
        "dashboard_api_key = false\n"
        "log_level = ERROR\n"
        "[Account]\n"
        "username = admin\n"
        f"password = {password_hash}\n"
        "enable_totp = false\n"
        "[Database]\n"
        "type = sqlite\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    application = create_app()
    gunicorn_settings = runpy.run_path(
        str(Path(__file__).parents[1] / "src" / "gunicorn.conf.py")
    )

    assert application.config["WGD_CONFIG"]["server"]["port"] == "19000"
    assert application.config["WGD_CONFIG"]["server"]["hostname"] == "127.0.0.1"
    assert application.config["WGD_CONFIG"]["server"]["authentication_required"] is True
    assert application.config["WGD_CONFIG"]["server"]["wgdashboard_apikey"] is False
    assert gunicorn_settings["bind"] == "127.0.0.1:19000"
    assert gunicorn_settings["wsgi_app"] == "main:create_app()"
    assert gunicorn_settings["errorlog"] == "log/error_gunicorn.log"
    assert gunicorn_settings["pidfile"] == "gunicorn.pid"
    assert (tmp_path / "secret_key").is_file()


def test_update_check_handles_network_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    def raise_network_error(*args: object, **kwargs: object) -> None:
        raise URLError("unavailable")

    monkeypatch.setattr("urllib.request.urlopen", raise_network_error)

    assert utilities.update_info("1.0.0") == (False, False, "")


def test_protocols_enabled_uses_snake_case_name(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.DEBUG)

    def find_command(command_name: str) -> str | None:
        if command_name in {"wg", "wg-quick"}:
            return "/usr/bin/wg"
        return None

    monkeypatch.setattr("shutil.which", find_command)

    assert utilities.protocols_enabled() == ["wg"]
    assert not hasattr(utilities, "ProtocolsEnabled")
    assert "checking installed WireGuard protocols" in caplog.text


def test_alembic_upgrade_creates_schema_on_sqlite(tmp_path: Path) -> None:
    database_path = tmp_path / "migration.sqlite"
    alembic_config = Config(str(Path(__file__).parents[1] / "alembic.ini"))
    alembic_config.attributes["database_url"] = f"sqlite:///{database_path}"

    command.upgrade(alembic_config, "head")
    command.check(alembic_config)

    engine = create_engine(f"sqlite:///{database_path}")
    table_names = set(inspect(engine).get_table_names())
    engine.dispose()

    assert {
        "users",
        "apikeys",
        "wireguard_interfaces",
        "amnezia_interfaces",
        "interface_peers",
        "alembic_version",
    }.issubset(table_names)
