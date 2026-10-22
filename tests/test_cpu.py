
def test_cpu_usage_empty(client):
    response = client.get('/api/v1/cpu-usage')
    assert response.status_code == 400

def test_cpu_usage_per_cpu_true(client):
    response = client.get('/api/v1/cpu-usage?per-cpu=true')
    assert response.status_code == 200

def test_cpu_usage_per_cpu_false(client):
    response = client.get('/api/v1/cpu-usage?per-cpu=false')
    assert response.status_code == 200

def test_cpu_usage_invalid_parameter(client):
    response = client.get('/api/v1/cpu-usage?per-cpu=invalid')
    assert response.status_code == 400

def test_cpu_times(client):
    response = client.get('/api/v1/cpu-times')
    assert response.status_code == 200

def test_cpu_times_json_structure(client):
    response = client.get('/api/v1/cpu-usage?per-cpu=true')
    data = response.get_json()
    assert data is not None
    for cpu, stats in data.items():
        assert 'percent' in stats