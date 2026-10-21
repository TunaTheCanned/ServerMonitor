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

def test_disk_status_code(client):
    response = client.get('/api/v1/disk')
    assert response.status_code == 200

def test_health_check(client):
    response = client.get('/api/v1/health')
    assert response.status_code == 200

def test_process_info(client):
    response = client.get('/api/v1/processes')
    data = response.get_json()
    assert response.status_code == 200
    assert data is not None
    assert isinstance(data, dict)
    assert 'processes' in data
    assert isinstance(data['processes'], dict)
    for pid, process in data['processes'].items():
        assert 'pid' in process
        assert 'rss_bytes' in process
        assert 'name' in process
        assert 'status' in process