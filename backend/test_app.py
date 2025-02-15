import json
import pytest
from main import app, db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
        yield client


def test_create_user(client):
    response = client.post('/users', data=json.dumps({'name': 'Alice'}),
                           content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'Alice'


def test_get_users(client):
    # Create a user first
    client.post('/users', data=json.dumps({'name': 'Alice'}),
                content_type='application/json')
    response = client.get('/users')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['name'] == 'Alice'
