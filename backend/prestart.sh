#! /usr/bin/env bash

set -e
set -x

# Let the DB start
python backend_pre_start.py
export PYTHONPATH=/app:$PYTHONPATH
cd app
# Run migrations
alembic upgrade head
cd ..
# Create initial data in DB
python initial_data.py