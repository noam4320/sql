import pytest

from main import app


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def ttest_person_post(client):
    response = client.post('/person', json={"name": "johnsters", "email": "noamhkjjhkgkhgj8835@g"})
    assert response.status_code == 201


def ttest_person_patch(client):
    response = client.patch('/person/1', json={"name": "yair"})
    assert response.status_code == 200


def test_person_get(client):
    response = client.get('/person/1')
    assert response.status_code == 200


def ttest_person_delete(client):
    client.post('/person', json={"name": "noam",  "email": "juygnggjh@g"})
    response = client.delete('/person/1')
    assert response.status_code == 200
