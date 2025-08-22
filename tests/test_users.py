import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from sqlalchemy.engine.url import URL
#from alembic import command

# ---- DB setup ----
SQLALCHEMY_DATABASE_URL = URL.create(
    drivername="postgresql",
    username=settings.database_username,
    password=settings.database_password,
    host=settings.database_hostname,
    port=settings.database_port,
    database=f"{settings.database_name}_test",
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ---- setup/teardown DB ----
@pytest.fixture(scope="module", autouse=True)
def create_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    #command.downgrade("base")  # to reset migrations
    #command.upgrade("head")   # to apply migrations
    
    yield
    #Base.metadata.drop_all(bind=engine)

# ---- override ----
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# ---- tests ----
def test_read_main():
    response = client.get("/")
    assert response.json() == {"message": "Oussama Hello, FastAPI is working!"}
    assert response.status_code == 200


def test_create_user():
    email = f"test_{uuid.uuid4().hex}@example.com"  # unique email
    response = client.post(
        "/users/",
        json={"email": email, "password": "string123"}
    )
    new_user = schemas.User(**response.json())
    assert new_user.email == email
    assert response.status_code == 201


def test_create_and_get_user():
    email = f"test_{uuid.uuid4().hex}@example.com"
    password = "string123"

    # ---- create user ----
    response = client.post(
        "/users/",
        json={"email": email, "password": password}
    )
    new_user = schemas.User(**response.json())
    assert new_user.email == email
    assert response.status_code == 201

    user_id = new_user.id  # ناخد id بتاع اليوزر الجديد

    # ---- login user ----
    login_response = client.post(
        "/login",
        data={"username": email, "password": password}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # ---- GET /users/{id} ----
    protected_response = client.get(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert protected_response.status_code == 200
    data = protected_response.json()
    assert data["email"] == email
    assert data["id"] == user_id
