#!/bin/bash

set -euo pipefail

if [ "dev" = $ENV_MODE ]; then
    flask db upgrade
fi

gunicorn -b 0.0.0.0:5000 app:app

exec "$@"ß