#!/bin/bash
set -a # set allexport so that the sourced .env vars are exported
. .env

docker compose up --build --remove-orphans

set +a # unset allexport
