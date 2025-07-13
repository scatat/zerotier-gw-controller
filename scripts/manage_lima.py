zerotier-gw-controller/scripts/manage_lima.py
#!/usr/bin/env python3
"""
manage_lima.py - Automate Lima VM lifecycle and ZeroTier Gateway Controller build/test workflow.

Features:
- Create/start Lima VM (Ubuntu 22.04 by default) if not present
- Copy project repo into VM
- Run build/install/test commands inside VM
- Optionally nuke (delete) the VM after completion (controlled by --nuke/--no-nuke)
- Fast feedback loop for packaging and install testing

Usage:
    python3 scripts/manage_lima.py [--nuke | --no-nuke] [--vm-name NAME] [--repo-path PATH]

Requirements:
- lima installed (`brew install lima`)
- Python 3.8+
"""

import argparse
import subprocess
import sys
import os
import shutil

DEFAULT_VM_NAME = "zt-gw-test"
DEFAULT_LIMA_CONFIG = """
#cloud-config
hostname: zt-gw-test
users:
  - name: ubuntu
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    groups: sudo
    ssh-authorized-keys:
      - {ssh_key}
"""
DEFAULT_IMAGE = "ubuntu:22.04"
DEFAULT_REPO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def run(cmd, check=True, capture_output=False, shell=False):
    """Run a shell command and print output."""
    print(f"\033[1;34m$ {cmd}\033[0m")
    result = subprocess.run(cmd, shell=shell, check=check, capture_output=capture_output, text=True)
    if capture_output:
        return result.stdout.strip()
    return None

def lima_exists(vm_name):
    """Check if Lima VM exists."""
    try:
        output = run(["limactl", "list", "--format", "json"], capture_output=True)
        import json
        vms = json.loads(output)
        return any(vm["name"] == vm_name for vm in vms)
    except Exception:
        return False

def lima_running(vm_name):
    """Check if Lima VM is running."""
    try:
        output = run(["limactl", "list", "--format", "json"], capture_output=True)
        import json
        vms = json.loads(output)
        for vm in vms:
            if vm["name"] == vm_name:
                return vm["status"] == "Running"
        return False
    except Exception:
        return False

def create_lima_vm(vm_name):
    """Create Lima VM with default config."""
    print(f"Creating Lima VM '{vm_name}'...")
    ssh_pubkey = run(["cat", os.path.expanduser("~/.ssh/id_rsa.pub")], capture_output=True)
    config_path = f"/tmp/{vm_name}-lima.yaml"
    with open(config_path, "w") as f:
        f.write(DEFAULT_LIMA_CONFIG.format(ssh_key=ssh_pubkey))
    run([
        "limactl", "start", "--name", vm_name, "--set", f"images[0].arch=amd64", "--set", f"images[0].image={DEFAULT_IMAGE}", config_path
    ])
    os.remove(config_path)

def start_lima_vm(vm_name):
    """Start Lima VM if stopped."""
    print(f"Starting Lima VM '{vm_name}'...")
    run(["limactl", "start", vm_name])

def stop_lima_vm(vm_name):
    """Stop Lima VM."""
    print(f"Stopping Lima VM '{vm_name}'...")
    run(["limactl", "stop", vm_name])

def delete_lima_vm(vm_name):
    """Delete Lima VM."""
    print(f"Nuking Lima VM '{vm_name}'...")
    run(["limactl", "delete", "--force", vm_name])

def copy_repo_to_vm(vm_name, repo_path):
    """Copy repo into Lima VM using limactl copy."""
    print(f"Copying repo '{repo_path}' into VM '{vm_name}'...")
    # Copy to /home/ubuntu/zerotier-gw-controller
    run([
        "limactl", "copy", repo_path, f"{vm_name}:/home/ubuntu/zerotier-gw-controller"
    ])

def run_in_vm(vm_name, command, workdir="/home/ubuntu/zerotier-gw-controller"):
    """Run a shell command inside the Lima VM."""
    full_cmd = f"cd {workdir} && {command}"
    run([
        "limactl", "shell", vm_name, "bash", "-c", full_cmd
    ])

def main():
    parser = argparse.ArgumentParser(description="Manage Lima VM for ZeroTier Gateway Controller build/test.")
    parser.add_argument("--nuke", action="store_true", help="Delete the VM after completion")
    parser.add_argument("--no-nuke", action="store_true", help="Do not delete the VM after completion (default)")
    parser.add_argument("--vm-name", type=str, default=DEFAULT_VM_NAME, help="Name of the Lima VM")
    parser.add_argument("--repo-path", type=str, default=DEFAULT_REPO_PATH, help="Path to project repo to copy")
    args = parser.parse_args()

    vm_name = args.vm_name
    repo_path = os.path.abspath(args.repo_path)
    nuke_vm = args.nuke and not args.no_nuke

    # 1. Create/start VM if needed
    if not lima_exists(vm_name):
        create_lima_vm(vm_name)
    elif not lima_running(vm_name):
        start_lima_vm(vm_name)
    else:
        print(f"Lima VM '{vm_name}' already running.")

    # 2. Copy repo into VM
    copy_repo_to_vm(vm_name, repo_path)

    # 3. Run build/install/test commands inside VM
    print("\n=== Running build/install/test commands in VM ===\n")
    try:
        # Install dependencies
        run_in_vm(vm_name, "sudo apt-get update && sudo apt-get install -y python3 python3-requests python3-yaml iputils-ping dpkg-dev debhelper python3-setuptools")
        # Build package
        run_in_vm(vm_name, "./scripts/build-deb.sh")
        # Install package
        run_in_vm(vm_name, "sudo dpkg -i ../zerotier-gateway-controller_1.0.0_all.deb")
        # Run tests
        run_in_vm(vm_name, "pytest tests")
        print("\n\033[1;32mAll build/install/test steps completed successfully.\033[0m\n")
    except subprocess.CalledProcessError as e:
        print(f"\n\033[1;31mError during build/install/test: {e}\033[0m\n")
        if nuke_vm:
            print("Nuking VM due to error.")
            delete_lima_vm(vm_name)
        sys.exit(1)

    # 4. Optionally nuke VM
    if nuke_vm:
        delete_lima_vm(vm_name)
    else:
        print(f"\nVM '{vm_name}' left running for further inspection. Use --nuke to delete after run.")

if __name__ == "__main__":
    main()
