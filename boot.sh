#!/bin/sh

# Ensure the prometheus multiprocess directory exists
if [ -n "$PROMETHEUS_MULTIPROC_DIR" ]; then
    mkdir -p "$PROMETHEUS_MULTIPROC_DIR"
fi

# No need to source .venv in Docker as packages are installed globally
while true; do
    flask db upgrade
    if [ "$?" = "0" ]; then
        break
    fi
    echo "Upgrade command failed, retrying in 5 secs..."
    sleep 5
done

exec gunicorn -b :5000 \
  --access-logfile - \
  --error-logfile - \
  -c gunicorn_config.py \
  microblog:app
