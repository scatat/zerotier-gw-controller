# ZeroTier Gateway Controller: Installation Guide

This guide describes how to install and set up the ZeroTier Gateway Controller on your system.

---

## Prerequisites

- **Operating System:** Ubuntu 18.04+, Debian 10+, or compatible Linux
- **Python:** Version 3.8 or newer
- **ZeroTier:** Active ZeroTier network and API token
- **Dependencies:** `python3-requests`, `python3-yaml`, `iputils-ping`
- **Permissions:** Ability to install packages and manage systemd services

---

## Installation Methods

### 1. **Development Install (Recommended for Testing)**

Clone the repository and install in editable mode:

```bash
git clone https://github.com/your-org/zerotier-gw-controller.git
cd zerotier-gw-controller
pip install -e .
```

### 2. **Debian Package (.deb) Install**

> **Note:** This method is for production deployment on Debian/Ubuntu systems.

1. Build the package (or download from releases):

    ```bash
    ./scripts/build-deb.sh
    ```

2. Install the package:

    ```bash
    sudo dpkg -i zerotier-gateway-controller_1.0.0_all.deb
    ```

3. The installer will:
    - Create a system user `zerotier-controller`
    - Install files to `/usr/lib/python3/dist-packages/zerotier_gateway_controller/`
    - Place config at `/etc/zerotier-gateway-controller/config.yaml`
    - Set up systemd service

### 3. **PyPI Install (Planned)**

Once published:

```bash
pip install zerotier-gateway-controller
```

---

## Configuration

Copy and edit the example config file:

```bash
sudo cp debian/config.yaml.example /etc/zerotier-gateway-controller/config.yaml
sudo chmod 600 /etc/zerotier-gateway-controller/config.yaml
```

Edit the config file to set your ZeroTier API token, network ID, gateways, and other options.

See [`docs/configuration.md`](configuration.md) for full details.

---

## Running the Controller

### **Manual Run (Development)**

```bash
python -m zerotier_gateway_controller.cli --config /etc/zerotier-gateway-controller/config.yaml
```

### **Systemd Service (Production)**

Enable and start the service:

```bash
sudo systemctl enable zerotier-gateway-controller
sudo systemctl start zerotier-gateway-controller
```

Check status and logs:

```bash
sudo systemctl status zerotier-gateway-controller
sudo journalctl -u zerotier-gateway-controller
```

---

## Uninstallation

To remove the package and service:

```bash
sudo systemctl stop zerotier-gateway-controller
sudo apt-get remove zerotier-gateway-controller
sudo userdel zerotier-controller
sudo rm -rf /etc/zerotier-gateway-controller/
```

---

## Troubleshooting

- **Missing dependencies:** Install with `sudo apt-get install python3-requests python3-yaml iputils-ping`
- **Permission errors:** Ensure config file is readable by `zerotier-controller` user
- **Service not starting:** Check logs with `journalctl -u zerotier-gateway-controller`
- **API errors:** Verify ZeroTier API token and network ID

---

## Next Steps

- Configure your gateways and test failover
- Integrate with Ansible for automated deployment (see progress log)
- Refer to [`docs/progress.md`](progress.md) for development status

---