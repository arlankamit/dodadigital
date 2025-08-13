#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/backend"
uvicorn main:app --reload
