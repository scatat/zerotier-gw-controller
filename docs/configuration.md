# ZeroTier Gateway Controller: Configuration Reference

This document describes all configuration options for the ZeroTier Gateway Controller. The configuration file is written in YAML and controls gateway monitoring, failover logic, API credentials, logging, and optional monitoring integrations.

---

## Configuration File Locations

- **System-wide:** `/etc/zerotier-gateway-controller/config.yaml`
- **User-specific:** `~/.config/zerotier-gateway-controller/config.yaml`
- **CLI override:** `--config /path/to/config.yaml`

---

## Example Configuration

```yaml
zerotier:
  api_token: "zt_api_token_here"     # ZeroTier Central API token (required)
  network_id: "network_id_here"      # ZeroTier network ID (required)
  home_subnet: "10.0.1222.0/24"      # Target home subnet to route (required)

grafana:                             # Optional Grafana Cloud Loki integration
  loki_url: "https://logs-prod-XX.grafana.net/loki/api/v1/push"
  api_key: "grafana_api_key_here"

gateways:
  - name: "kingdok"                  # Primary gateway
    ip: "172.23.0.1"
    priority: 1
  - name: "fone"                     # Backup gateway
    ip: "172.23.0.2"
    priority: 2

check_interval: 60                   # Health check interval (seconds, default: 60)
log_level: "INFO"                    # Logging verbosity: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

---

## Option Reference

### `zerotier`
- **api_token**: *(string, required)*  
  ZeroTier Central API token. Obtain from ZeroTier Central web interface.
- **network_id**: *(string, required)*  
  The ZeroTier network ID to manage.
- **home_subnet**: *(string, required)*  
  The target subnet to route (e.g., `10.0.1222.0/24`).

### `grafana`
- **loki_url**: *(string, optional)*  
  Grafana Loki push API endpoint for log streaming.
- **api_key**: *(string, optional)*  
  Grafana Loki API key for authentication.

### `gateways`
- **name**: *(string, required)*  
  Human-readable name for the gateway.
- **ip**: *(string, required)*  
  ZeroTier network IP address of the gateway.
- **priority**: *(integer, required)*  
  Lower number = higher priority. Controller prefers lower-priority gateways.

### `check_interval`
- *(integer, optional, default: 60)*  
  Interval in seconds between health checks.

### `log_level`
- *(string, optional, default: "INFO")*  
  Logging verbosity. One of: DEBUG, INFO, WARNING, ERROR, CRITICAL.

---

## Notes

- All fields under `zerotier` and at least one gateway under `gateways` are required.
- If `grafana` is omitted, monitoring integration is disabled.
- The controller only manages the route for `home_subnet`; other routes are preserved.
- For best security, restrict config file permissions to owner read/write (`chmod 600`).

---

## Troubleshooting

- **Missing config file:** Controller will exit with an error.
- **Invalid YAML:** Parse errors will include line numbers.
- **Missing required fields:** Controller will log a clear error and exit.
- **API authentication errors:** Check `api_token` and network permissions.

---

## Updating Configuration

- Edit the config file and restart the controller service.
- Live reload is not currently supported.

---

For further details, see the [README](../README.md) and [progress log](progress.md).