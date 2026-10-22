
def test_disk_status_code(client):
    response = client.get('/api/v1/disk')
    assert response.status_code == 200

def test_disk_json_structure(client):
    response = client.get('/api/v1/disk')
    data = response.get_json()
    assert data is not None
    for partition, stats in data.items():
        assert 'free' in stats
        assert 'used' in stats
        assert 'total' in stats
        assert 'percent' in stats