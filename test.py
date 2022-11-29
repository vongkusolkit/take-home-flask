import pytest
from main import app as flask_app


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


def test_balance_no_transactions(client):
    response = client.get('http://127.0.0.1:5000/balances')
    print(response.data)
    expected = '{}'
    decoded_response = response.data.decode('utf-8').rstrip('\n')
    assert decoded_response == expected
    assert response.status_code == 200


def test_add_transaction(client):
    response = client.post('http://127.0.0.1:5000/transaction',
                           json={"payer": "DANNON", "points": 300, "timestamp": "2022-10-31T10:00:00Z"})
    assert response.status_code == 200

    response = client.post('http://127.0.0.1:5000/transaction',
                           json={"payer": "UNILEVER", "points": 200, "timestamp": "2022-10-31T11:00:00Z"})
    assert response.status_code == 200

    response = client.post('http://127.0.0.1:5000/transaction',
                           json={"payer": "DANNON", "points": -200, "timestamp": "2022-10-31T15:00:00Z"})
    assert response.status_code == 200

    response = client.post('http://127.0.0.1:5000/transaction',
                           json={"payer": "MILLER COORS", "points": 10000, "timestamp": "2022-11-01T14:00:00Z"})
    assert response.status_code == 200

    response = client.post('http://127.0.0.1:5000/transaction',
                           json={"payer": "DANNON", "points": 1000, "timestamp": "2022-11-02T14:00:00Z"})
    assert response.status_code == 200


def test_add_transaction_error(client):
    response = client.post('http://127.0.0.1:5000/transaction',
                           json={"payer": "DANNON", "points": 50.2, "timestamp": "2022-11-02T14:00:00Z"})
    assert response.status_code == 400

    response = client.post('http://127.0.0.1:5000/transaction',
                           json={"payer": "DANNON", "points": 'a', "timestamp": "2022-11-02T14:00:00Z"})
    assert response.status_code == 400

    response = client.post('http://127.0.0.1:5000/transaction',
                           json={"payer": "DANNON", "points": 1000, "timestamp": "2022/11"})
    assert response.status_code == 400


def test_spend_points(client):
    response = client.post('http://127.0.0.1:5000/points', json={"points": 5000})
    expected = '[{"payer":"DANNON","points":-100},{"payer":"UNILEVER","points":-200},{"payer":"MILLER COORS","points":-4700}]'
    decoded_response = response.data.decode('utf-8').rstrip('\n')
    assert decoded_response == expected
    assert response.status_code == 200


def test_spend_points_error(client):
    response = client.post('http://127.0.0.1:5000/points', json={"points": 500000})
    assert response.status_code == 400
    response = client.post('http://127.0.0.1:5000/points', json={"points": -100})
    assert response.status_code == 400


def test_balance(client):
    response = client.get('http://127.0.0.1:5000/balances')
    print(response.data)
    expected = '{"DANNON":1000,"MILLER COORS":5300,"UNILEVER":0}'
    decoded_response = response.data.decode('utf-8').rstrip('\n')
    assert decoded_response == expected
    assert response.status_code == 200
