#!/usr/bin/env bash


conda activate kodexa
datamodel-codegen --input kodexa-swagger.json --output kodexa_cloud/model.py --target-python-version 3.6