#!/bin/bash
PYTHONPATH=./src
export PYTHONPATH
coverage run --branch --omit *exifread* -m unittest discover -s tests -v

