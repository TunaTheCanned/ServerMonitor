
def test_cores_logical_empty(client):
    response = client.get('/api/v1/cores')
    assert response.status_code == 400

def test_cores_logical_true(client):
    response = client.get('/api/v1/cores?logical=true')
    assert response.status_code == 200

def test_cores_logical_false(client):
    response = client.get('/api/v1/cores?logical=false')
    assert response.status_code == 200

def test_cores_logical_invalid_parameter(client):
    response = client.get('/api/v1/cores?logical=invalid')
    assert response.status_code == 400

def test_cores_json_structure(client):
    response = client.get('/api/v1/cores?logical=true')
    data = response.get_json()
    assert 'cores' in data