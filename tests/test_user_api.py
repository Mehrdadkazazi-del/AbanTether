import uuid
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def unique_national_code():
    return str(uuid.uuid4().int)[:10]


def test_add_user_success(unique_national_code):
    response = client.post(
        "/user/addUser/",
        json={
            "firstName": "unitTest",
            "lastName": "unitTest",
            "nationalCode": unique_national_code,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["firstName"] == "unitTest"
    assert data["lastName"] == "unitTest"
    assert data["nationalCode"] == unique_national_code


def test_add_user_duplicate_national_code():
    duplicate_code = "1234567890"

    first_response = client.post(
        "/user/addUser/",
        json={
            "firstName": "unitTest",
            "lastName": "unitTest",
            "nationalCode": duplicate_code,
        },
    )
    assert first_response.status_code == 200

    second_response = client.post(
        "/user/addUser/",
        json={
            "firstName": "unitTest",
            "lastName": "unitTest",
            "nationalCode": duplicate_code,
        },
    )
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "National code already exists"


def test_add_user_invalid_data():
    """Test adding a user with invalid data."""
    invalid_data = [
        {"firstName": "", "lastName": "unitTest", "nationalCode": "12345"},  # Empty first name
        {"firstName": "unitTest", "lastName": "", "nationalCode": "1234567890"},  # Empty last name
        {"firstName": "unitTest", "lastName": "unitTest", "nationalCode": ""},  # Empty national code
        {"firstName": "unitTest", "lastName": "unitTest", "nationalCode": "123"},  # Invalid length
    ]

    for data in invalid_data:
        response = client.post("/user/addUser/", json=data)
        assert response.status_code == 400
        assert "Invalid data" in response.json()["detail"]
