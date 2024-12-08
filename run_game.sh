#!/bin/bash

# Activate virtual envinronment and install dependencies
poetry install
poetry shell

# Run the game
python src/main.py
