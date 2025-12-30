#!/bin/sh
set -e

# Source Nix profile
if [ -f /root/.nix-profile/etc/profile.d/nix.sh ]; then
    . /root/.nix-profile/etc/profile.d/nix.sh
fi

# Add per-user Nix profile to PATH
export PATH="/nix/var/nix/profiles/per-user/root/profile/bin:$PATH"

# Execute the command passed to the script
exec "$@"
