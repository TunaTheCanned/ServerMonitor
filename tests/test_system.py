
def test_uptime_status_code(client):
    response = client.get('/api/v1/uptime')
    assert response.status_code == 200

def test_uptime_json_structure(client):
    response = client.get('/api/v1/uptime')
    data = response.get_json()
    assert 'uptime_seconds' in data

def test_load_status_code(client):
    response = client.get('/api/v1/load')
    assert response.status_code == 200

def test_load_json_structure(client):
    response = client.get('/api/v1/load')
    data = response.get_json()
    assert data is not None
    data = data['system load']
    assert 'load_1' in data
    assert 'load_5' in data
    assert 'load_15' in data

def test_system_status_code(client):
    response = client.get('/api/v1/system')
    assert response.status_code == 200

def test_system_json_structure(client):
    response = client.get('/api/v1/system')
    data = response.get_json()
    assert 'system' in data
    assert 'version' in data
    assert 'architecture' in data
