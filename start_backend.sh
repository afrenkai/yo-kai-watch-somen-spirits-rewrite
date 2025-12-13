#!/bin/bash

set -e

echo "Starting backend server..."

cd backend

uv run uvicorn main:socket_app --reload --host 0.0.0.0 --port 8000
