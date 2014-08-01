#!/bin/bash
PYTHONPATH=./src
export PYTHONPATH
python -m unittest discover -s tests -v

