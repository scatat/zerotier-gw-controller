# ZeroTier Gateway Controller

## Overview

**ZeroTier Gateway Controller** is a Python-based service that automates failover and route management for ZeroTier mesh network gateways. It ensures high-availability access to your home subnet by monitoring gateway health and dynamically updating ZeroTier network routes via the ZeroTier Central API.

- **Primary Use Case:** Seamless, automatic failover between gateway nodes for remote access to a home LAN.
- **Key Features:** Health monitoring, priority-based failover, dynamic route updates, logging, and optional Grafana Cloud integration.

---

## Architecture

### Network Layout

- **Home Subnet:** `10.0.1222.0/24` (private LAN)
- **ZeroTier Network:** `172.23.0.0/16` (mesh overlay)
- **Gateway Nodes:**  
  - `kingdok` (`172.23.0.1`) – primary  
  - `fone` (`172.23.0.2`) – backup
- **Controller Node:**  
  - `phoney` (`172.23.0.3`) – runs controller, monitors gateways
- **Client Nodes:**  
  - e.g., `macbook` (`172.23.0.x`) – needs access to home subnet

### How It Works

1. **Health Checks:** Controller pings gateways on the ZeroTier network.
2. **Failover:** If the primary gateway fails, controller updates ZeroTier route to use backup.
3. **Route Management:** Only the home subnet route is managed; other routes are preserved.
4. **Logging & Monitoring:** All actions are logged; optional integration with Grafana Cloud Loki.

---

## Quick Start

### Prerequisites

- Python 3.8+
- ZeroTier network with API access
- Gateway nodes bridging ZeroTier to home subnet
- `iputils-ping` installed on controller node

### Installation (Development)

```bash
git clone https://github.com/your-org/zerotier-gw-controller.git
cd zerotier-gw-controller
pip install -e .
```

### Configuration

Create a config file (see `debian/config.yaml.example`):

```yaml
zerotier:
  api_token: "zt_api_token_here"
  network_id: "network_id_here"
  home_subnet: "10.0.1222.0/24"

gateways:
  - name: "kingdok"
    ip: "172.23.0.1"
    priority: 1
  - name: "fone"
    ip: "172.23.0.2"
    priority: 2

check_interval: 60
log_level: "INFO"
```

### Running the Controller

```bash
python -m zerotier_gateway_controller.cli --config /path/to/config.yaml
```

---

## Progress & Development

See [`docs/progress.md`](docs/progress.md) for ongoing development notes, issues, and next steps.

---

## Documentation

- **Installation Guide:** [`docs/installation.md`](docs/installation.md)
- **Configuration Reference:** [`docs/configuration.md`](docs/configuration.md)
- **API Integration:** See below and [`docs/api.md`](docs/api.md)

---

## License

MIT License. See [`LICENSE`](LICENSE) for details.

---

## Contributing

Pull requests and issues welcome! See [`docs/progress.md`](docs/progress.md) for current status and open tasks.

---