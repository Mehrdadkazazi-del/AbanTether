from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_pay_order_success():
    order_data = {
        "user_id": "123",
        "crypto_name": "ABAN",
        "amount": "10",
        "price_per_unit": "4"
    }

    response = client.post("/order/payOrder/", json=order_data)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["order_id"] == 1
    assert response_data["status"]
