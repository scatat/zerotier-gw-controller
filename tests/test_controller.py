import pytest

# Import the controller module (will fail until implemented)
try:
    from zerotier_gateway_controller import controller
except ImportError:
    controller = None

def test_import_controller():
    """Test that the controller module can be imported."""
    assert controller is not None, "controller module should be importable"

def test_is_gateway_reachable_stub(monkeypatch):
    """Stub test for is_gateway_reachable function."""
    from zerotier_gateway_controller.controller import ZeroTierGatewayController, ControllerConfig

    config = {
        "zerotier": {
            "api_token": "dummy",
            "network_id": "dummy",
            "home_subnet": "10.0.122.0/24"
        },
        "gateways": [
            {"name": "kingdok", "ip": "172.23.0.1", "priority": 1},
            {"name": "fone", "ip": "172.23.0.2", "priority": 2}
        ],
        "check_interval": 60,
        "log_level": "INFO"
    }
    controller_instance = ZeroTierGatewayController(ControllerConfig(config))

    # Monkeypatch the instance method
    monkeypatch.setattr(controller_instance, "is_gateway_reachable", lambda ip: ip == "172.23.0.1")
    assert controller_instance.is_gateway_reachable("172.23.0.1") is True
    assert controller_instance.is_gateway_reachable("172.23.0.2") is False

def test_determine_active_gateway_stub(monkeypatch):
    """Stub test for determine_active_gateway function."""
    from zerotier_gateway_controller.controller import ZeroTierGatewayController, ControllerConfig

    config = {
        "zerotier": {
            "api_token": "dummy",
            "network_id": "dummy",
            "home_subnet": "10.0.122.0/24"
        },
        "gateways": [
            {"name": "kingdok", "ip": "172.23.0.1", "priority": 1},
            {"name": "fone", "ip": "172.23.0.2", "priority": 2}
        ],
        "check_interval": 60,
        "log_level": "INFO"
    }
    controller_instance = ZeroTierGatewayController(ControllerConfig(config))

    # Monkeypatch the instance method to simulate only fone is reachable
    monkeypatch.setattr(controller_instance, "is_gateway_reachable", lambda ip: ip == "172.23.0.2")
    active = controller_instance.determine_active_gateway()
    assert active.name == "fone"
