#!/bin/bash
# build-deb.sh - Build Debian package for ZeroTier Gateway Controller

set -e

PROJECT_ROOT="$(dirname "$(realpath "$0")")/.."
DEBIAN_DIR="$PROJECT_ROOT/debian"
PKG_NAME="zerotier-gateway-controller"
PKG_VERSION="1.0.0"
ARCH="all"

echo "Building Debian package for $PKG_NAME..."

# Clean previous builds
rm -rf "$PROJECT_ROOT/build" "$PROJECT_ROOT/dist" "$PROJECT_ROOT/${PKG_NAME}_*.deb"

# Ensure debian/ directory exists
if [ ! -d "$DEBIAN_DIR" ]; then
    echo "Error: debian/ directory not found!"
    exit 1
fi

# Build source distribution
cd "$PROJECT_ROOT"
python3 -m build

# Create Debian package
dpkg-buildpackage -us -uc -b

echo "Debian package build complete."
echo "Find your .deb file in the parent directory:"
ls -lh "$PROJECT_ROOT/../${PKG_NAME}_*.deb" || true
