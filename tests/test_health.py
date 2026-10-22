
def test_health_status_code(client):
    response = client.get('/api/v1/health')
    assert response.status_code == 200

def test_health_json_structure(client):
    response = client.get('/api/v1/health')
    data = response.get_json()
    assert 'overall' in data