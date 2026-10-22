
def test_process_info_no_sort(client):
    response = client.get("/api/v1/processes")
    assert response.status_code == 200

def test_process_info_sort_invalid(client):
    response = client.get("/api/v1/processes?sort-by=invalid")
    assert response.status_code == 400

def test_process_info_limit_invalid(client):
    response = client.get("/api/v1/processes?sort-by=cpu&limit=invalid")
    assert response.status_code == 400

def test_process_info_limit_negative(client):
    response = client.get("/api/v1/processes?sort-by=cpu&limit=-1")
    assert response.status_code == 400

def test_process_info_json_structure(client):
    response = client.get('/api/v1/processes?sort-by=cpu&limit=5')
    data = response.get_json()
    assert response.status_code == 200
    assert data is not None
    assert isinstance(data, dict)
    assert 'processes' in data
    for process in data["processes"]:
        assert 'pid' in process
        assert 'cpu_percent' in process
        assert 'rss_bytes' in process
        assert 'name' in process
        assert 'status' in process