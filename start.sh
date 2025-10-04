#!/bin/bash

python3 -m venv .venv
source .venv/bin/activate
pip install litellm python-dotenv
pip install -r requirements.txt
