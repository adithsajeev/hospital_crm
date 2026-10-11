from services.auth_utils import hash_password
from models.user import User

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_login_success(client, db_session):
    test_user = User(
        username="testadmin",
        email="a dmin@hospital.com",
        hashed_password=hash_password("admin123"),
        full_name="Admin User",
        role="admin",
        is_active=True
    )
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    response = client.post(
        "/auth/login",
        data={"username": "testadmin", "password": "admin123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_create_and_search_patient(client, db_session):
    test_user = User(
        username="receptionist1",
        email="receptionist@hospital.com",
        hashed_password=hash_password("pass123"),
        full_name="Receptionist Staff",
        role="receptionist",
        is_active=True
    )
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    login_res = client.post(
        "/auth/login",
        data={"username": "receptionist1", "password": "pass123"}
    )
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Match exact schema fields: phone & date_of_birth
    patient_payload = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "phone": "9876543210",
        "gender": "Female",
        "date_of_birth": "1995-05-15",
        "address": "123 Main St"
    }
    create_res = client.post("/patients/", json=patient_payload, headers=headers)
    assert create_res.status_code == 201
    assert create_res.json()["first_name"] == "Jane"

    search_res = client.get("/patients/?search=Jane", headers=headers)
    assert search_res.status_code == 200
    assert len(search_res.json()) == 1
    assert search_res.json()[0]["phone"] == "9876543210"