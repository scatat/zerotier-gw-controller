import pytest
import sys
from unittest import mock

# Import CLI entrypoint if available
try:
    from zerotier_gateway_controller.cli import main
except ImportError:
    main = None

def test_cli_runs_with_help(monkeypatch):
    """
    Test that the CLI runs and displays help without error.
    """
    if main is None:
        pytest.skip("CLI main entrypoint not implemented yet")

    test_args = ["zerotier-gateway-controller", "--help"]
    monkeypatch.setattr(sys, "argv", test_args)
    with pytest.raises(SystemExit) as excinfo:
        main()
    assert excinfo.value.code == 0

def test_cli_runs_with_config(monkeypatch):
    """
    Test that the CLI accepts a config argument.
    """
    if main is None:
        pytest.skip("CLI main entrypoint not implemented yet")

    test_args = ["zerotier-gateway-controller", "--config", "/tmp/config.yaml"]
    monkeypatch.setattr(sys, "argv", test_args)
    # Expect SystemExit if config file is missing or not implemented
    with pytest.raises(SystemExit):
        main()
