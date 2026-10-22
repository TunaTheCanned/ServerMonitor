
def test_network_status_code(client):
    response = client.get('/api/v1/network')
    assert response.status_code == 200