zerotier-gw-controller/src/zerotier_gateway_controller/cli.py#L1-38
import argparse
import sys
import logging
from zerotier_gateway_controller.controller import run_controller

def main():
    parser = argparse.ArgumentParser(
        description="ZeroTier Gateway Controller: Automated failover and route management for ZeroTier gateways."
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to configuration YAML file (default: system/user location)",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default=None,
        help="Override log level from config file",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run controller logic without making API changes (for testing)",
    )
    args = parser.parse_args()

    # Set up logging early
    log_level = args.log_level or "INFO"
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(asctime)s %(levelname)s %(message)s",
    )

    try:
        run_controller(
            config_path=args.config,
            log_level=args.log_level,
            dry_run=args.dry_run,
        )
    except Exception as e:
        logging.error(f"Controller failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
