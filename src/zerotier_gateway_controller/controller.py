zerotier-gw-controller/src/zerotier_gateway_controller/controller.py#L1-65
"""
ZeroTier Gateway Controller: Main Logic

This module implements the core health check, failover, and route management logic
for the ZeroTier Gateway Controller service.

Author: Stephen Tan
License: MIT
"""

import subprocess
import logging
import requests
import yaml
import time
from typing import List, Optional, Dict, Any

class Gateway:
    def __init__(self, name: str, ip: str, priority: int):
        self.name = name
        self.ip = ip
        self.priority = priority

class ControllerConfig:
    def __init__(self, config: Dict[str, Any]):
        self.zerotier_api_token = config["zerotier"]["api_token"]
        self.zerotier_network_id = config["zerotier"]["network_id"]
        self.home_subnet = config["zerotier"]["home_subnet"]
        self.gateways = [
            Gateway(gw["name"], gw["ip"], gw["priority"])
            for gw in config["gateways"]
        ]
        self.check_interval = config.get("check_interval", 60)
        self.log_level = config.get("log_level", "INFO")

class ZeroTierGatewayController:
    def __init__(self, config: ControllerConfig):
        self.config = config
        self.logger = logging.getLogger("ZeroTierGatewayController")
        self.logger.setLevel(self.config.log_level)

    def is_gateway_reachable(self, gateway_ip: str) -> bool:
        """
        Test gateway reachability using ping.
        - 2 ping packets with 3-second timeout.
        - Return True if any packet succeeds.
        """
        try:
            result = subprocess.run(
                ["ping", "-c", "2", "-W", "3", gateway_ip],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            return result.returncode == 0
        except Exception as e:
            self.logger.error(f"Ping failed for {gateway_ip}: {e}")
            return False

    def determine_active_gateway(self) -> Optional[Gateway]:
        """
        Priority-based gateway selection:
        1. Test gateways in priority order.
        2. Return first reachable gateway.
        3. If none reachable, return None.
        """
        sorted_gateways = sorted(self.config.gateways, key=lambda g: g.priority)
        for gw in sorted_gateways:
            if self.is_gateway_reachable(gw.ip):
                self.logger.info(f"Gateway {gw.name} ({gw.ip}) is reachable.")
                return gw
        self.logger.critical("No gateways are reachable!")
        return None

    def update_zerotier_route(self, gateway_ip: str) -> bool:
        """
        ZeroTier API interaction:
        1. GET current network configuration.
        2. Update home subnet route, preserve others.
        3. POST updated configuration.
        4. Handle API errors gracefully.
        """
        # Placeholder for API logic
        self.logger.info(f"Would update ZeroTier route to {gateway_ip}")
        return True

    def run(self):
        """
        Main controller loop.
        """
        self.logger.info("Starting ZeroTier Gateway Controller loop.")
        while True:
            active_gw = self.determine_active_gateway()
            if active_gw:
                self.update_zerotier_route(active_gw.ip)
            else:
                self.logger.critical("All gateways down. No route update performed.")
            time.sleep(self.config.check_interval)
