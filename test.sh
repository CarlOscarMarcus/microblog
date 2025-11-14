#!/bin/sh
set -e

cd /home/microblog

# Create venv fresh on each test run (safe with volume mounts)
if [ ! -d ".venv" ]; then
    python -m venv .venv
    .venv/bin/pip install --no-cache-dir -r requirements/test.txt
fi

. .venv/bin/activate

echo "Running tests..."
make test
echo "Tests finished. Container will stop."
exit 0
