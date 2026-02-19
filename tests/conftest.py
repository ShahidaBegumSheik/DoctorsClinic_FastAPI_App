import os
import sys
import importlib
from pathlib import Path
from urllib.parse import urlparse, urlunparse

import pytest
import uuid


TEST_DB_NAME = os.getenv("TEST_DB_NAME", "mydb_tests")


@pytest.fixture(scope="session")
def project_root() -> Path:
    root = Path(__file__).resolve().parents[1]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    return root


def _swap_db_name(url: str, db_name: str) -> str:
    parsed = urlparse(url)
    new_path = f"/{db_name}"
    return urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            new_path,
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )


@pytest.fixture(scope="session")
def test_db_url() -> str:
    explicit = os.getenv("TEST_DATABASE_URL")
    if explicit:
        return explicit

    base = os.getenv("DATABASE_URL")
    if base and base.startswith("postgres"):
        return _swap_db_name(base, TEST_DB_NAME)
    return f"postgresql://postgres:12345678@db:5432/{TEST_DB_NAME}"


@pytest.fixture(scope="session", autouse=True)
def _set_test_env(project_root: Path, test_db_url: str):
    os.environ["DATABASE_URL"] = test_db_url
    os.environ.setdefault("JWT_SECRET", "test-secret")
    os.environ.setdefault("ENV", "test")
    yield


@pytest.fixture(scope="session")
def fastapi_app(project_root: Path):
    import app.core.config as config
    importlib.reload(config)

    import app.db.session as session
    importlib.reload(session)

    import app.main as main_module
    importlib.reload(main_module)

    from app.db.base import Base
    Base.metadata.drop_all(bind=session.engine)
    Base.metadata.create_all(bind=session.engine)

    return main_module.app


@pytest.fixture()
def client(fastapi_app):
    from fastapi.testclient import TestClient

    with TestClient(fastapi_app) as c:
        yield c


def _register_admin(client, email: str | None = None, password: str = "Password123!"):
    if email is None:
        email = f"admin-{uuid.uuid4().hex[:10]}@example.com"
    res = client.post("/auth/register", json={"email": email, "password": password})
    assert res.status_code == 200, res.text
    return {"email": email, "password": password, "user": res.json()}


def _login(client, email: str, password: str) -> str:
    # OAuth2PasswordRequestForm expects form fields username/password.
    res = client.post(
        "/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert res.status_code == 200, res.text
    return res.json()["access_token"]


@pytest.fixture()
def admin_token(client) -> str:
    creds = _register_admin(client)
    return _login(client, creds["email"], creds["password"])


@pytest.fixture()
def admin_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}
