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


def test_create_user_missing_name(client):
    payload = json.dumps({})
    response = client.post('/users', data=payload, content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data
    assert data["error"] == "Name is required"


def test_get_single_user(client):
    response = client.post('/users', data=json.dumps({'name': 'Alice'}), content_type='application/json')
    user_id = json.loads(response.data)['id']
    response = client.get(f'/users/{user_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["id"] == user_id
    assert data["name"] == "Alice"


def test_update_user(client):
    # Create a user
    response = client.post('/users', data=json.dumps({'name': 'Alice'}), content_type='application/json')
    user_id = json.loads(response.data)['id']

    # Update the user’s name
    update_payload = json.dumps({'name': 'Alice Updated'})
    response = client.put(f'/users/{user_id}', data=update_payload, content_type='application/json')

    # Expect 200 OK response
    assert response.status_code == 200
    data = json.loads(response.data)

    # Check that the user was updated correctly
    assert data['id'] == user_id
    assert data['name'] == 'Alice Updated'


def test_delete_user(client):
    # Create a user
    response = client.post('/users', data=json.dumps({'name': 'Alice'}), content_type='application/json')
    user_id = json.loads(response.data)['id']

    # Delete the user
    response = client.delete(f'/users/{user_id}')
    
    # Expect 204 No Content response (or 200 OK with a message)
    assert response.status_code == 204

    # Try to retrieve the deleted user (should return 404)
    response = client.get(f'/users/{user_id}')
    assert response.status_code == 404
