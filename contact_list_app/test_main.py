from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .main import app, get_db
from .database import Base


client = TestClient(app)

# Setup the in-memory SQLite database for testing
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to override the get_db dependency in the main app
def override_get_db():
    database = TestingSessionLocal()
    yield database
    database.close()

app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=engine)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_create_group():
    response = client.post("/api/v1/groups", json={"name": "Test Group"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test Group"
    assert "id" in data


def test_read_group():
    response = client.get("/api/v1/groups/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test Group"
    assert "id" in data


def test_update_group():
    response = client.put("/api/v1/groups/1", json={"name": "Updated Test Group"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Updated Test Group"


def test_create_contact():
    response = client.post("/api/v1/contacts", json={
        "first_name": "Jean",
        "last_name": "Bonneau",
        "phone_number": "0612345678",
        "email": "jb@example.com",
        "group_id": 1,
        })
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["first_name"] == "Jean"
    assert data["last_name"] == "Bonneau"
    assert data["phone_number"] == "0612345678"
    assert data["email"] == "jb@example.com"
    assert data["group_id"] == 1
    assert "id" in data


def test_read_contact():
    response = client.get("/api/v1/contacts/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["first_name"] == "Jean"
    assert data["last_name"] == "Bonneau"
    assert data["phone_number"] == "0612345678"
    assert data["email"] == "jb@example.com"
    assert data["group_id"] == 1
    assert "id" in data


def test_update_contact():
    response = client.patch("/api/v1/contacts/1", json={
        "first_name": "Jean_u",
        "last_name": "Bonneau_u",
        "phone_number": "0612345670",
        "email": "jb_u@example.com",
        })
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["first_name"] == "Jean_u"
    assert data["last_name"] == "Bonneau_u"
    assert data["phone_number"] == "0612345670"
    assert data["email"] == "jb_u@example.com"


def test_update_contact_partial():
    response = client.patch("/api/v1/contacts/1", json={
        "phone_number": "0606060606",
        })
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["phone_number"] == "0606060606"
    assert "first_name" in data
    assert "last_name" in data
    assert "email" in data
    assert "group_id" in data
    assert "id" in data


def test_delete_contact():
    response = client.delete("/api/v1/contacts/1")
    assert response.status_code == 200, response.text
    data = response.json()
    "deleted" in data


def test_delete_group():
    response = client.delete("/api/v1/groups/1")
    assert response.status_code == 200, response.text
    data = response.json()
    "deleted" in data


def teardown():
    # Drop the tables in the test database
    Base.metadata.drop_all(bind=engine)