#!/bin/sh
# Import an archive produced by save.sh without contacting a registry.
set -eu
docker image load -i "${1:-crapi-images.tar}"
