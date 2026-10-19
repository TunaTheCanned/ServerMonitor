from collections import namedtuple

from app import metrics


def test_temperature_not_supported(monkeypatch):
    monkeypatch.delattr(metrics.psutil,"sensors_temperatures",raising=False)
    result = metrics.get_hardware_temperature()
    assert result["available"] is False
    assert result["reason"] == "Not supported on this OS"


def test_temperature_no_data(monkeypatch):
    monkeypatch.setattr(metrics.psutil,"sensors_temperatures",lambda fahrenheit=False: {}, raising=False)
    result = metrics.get_hardware_temperature()
    assert result["available"] is False
    assert result["reason"] == "No temperature sensor detected"


def test_temperature_read_error(monkeypatch):
    def raise_error(fahrenheit=False):
        raise OSError("Sensor read failed")
    monkeypatch.setattr(metrics.psutil,"sensors_temperatures",raise_error,raising=False)
    result = metrics.get_hardware_temperature()
    assert result["available"] is False
    assert "Sensor read failed" in result["reason"]


def test_temperature_success(monkeypatch):
    SensorReading = namedtuple("SensorReading",["label", "current", "high", "critical"])
    reading = SensorReading("Core 0", 45.0, 80.0, 100.0)
    monkeypatch.setattr(metrics.psutil,"sensors_temperatures",lambda fahrenheit=False: {"coretemp": [reading]},raising=False)
    result = metrics.get_hardware_temperature()
    assert result["available"] is True
    assert "coretemp" in result["sensors"]
    assert len(result["sensors"]["coretemp"]) == 1
    assert result["sensors"]["coretemp"][0]["current"] == 45.0