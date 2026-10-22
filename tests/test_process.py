
def test_process_info_status_code(client):
    response = client.get('/api/v1/processes')
    assert response.status_code == 200

def test_process_info_json_structure(client):
    response = client.get('/api/v1/processes')
    data = response.get_json()
    assert data is not None
    assert isinstance(data, dict)
    assert 'processes' in data
    assert isinstance(data['processes'], dict)
    for pid, process in data['processes'].items():
        assert 'pid' in process
        assert 'rss_bytes' in process
        assert 'name' in process
        assert 'status' in process