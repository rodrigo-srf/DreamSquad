#!/usr/bin/env bash
set -e

python -m venv .venv
source .venv/bin/activate 2>/dev/null || source .venv/Scripts/activate
pip install -r requirements.txt

[ ! -f .env ] && cp .env.example .env

uvicorn main:app --reload
