#!/bin/sh
# Export the images used by the local Compose stack, including its dependencies.
set -eu
archive=${1:-crapi-images.tar}
compose_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
images=$(docker compose --project-directory "$compose_dir" -f "$compose_dir/docker-compose.yml" config --images)
# Compose emits one image reference per line; image references cannot contain spaces.
docker image save -o "$archive" $images
