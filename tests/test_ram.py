
def test_memory_status_code(client):
    response = client.get('/api/v1/memory')
    assert response.status_code == 200

def test_memory_json_structure(client):
    response = client.get('/api/v1/memory')
    data = response.get_json()
    assert data is not None
    assert isinstance(data, dict)
    assert 'total' in data
    assert 'available' in data
    assert 'free' in data
    assert 'used' in data
    assert 'percent' in data
