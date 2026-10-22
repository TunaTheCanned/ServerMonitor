from app import metrics

def test_process_info_endpoint(client, monkeypatch):
    sample = {"processes":
                  [{"pid": 1234,
                    "name": "example.exe",
                    "status": "running",
                    "rss_bytes": 4096,
                    "cpu_percent": 12.5}]}

    def fake_process_info(sort_by, limit):
        return sample
    monkeypatch.setattr(metrics, "get_process_info", fake_process_info)
    response = client.get('/api/v1/processes?sort-by=cpu&limit=10')
    data = response.get_json()
    assert data == sample
    assert response.status_code == 200
