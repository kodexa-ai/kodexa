#!/bin/bash

rm -rf .swagger_tmp

swagger-codegen generate \
  -i https://quantum.kodexa.com/v2/api-docs \
  -l python \
  -o ./.swagger_tmp \
  -c swagger-config.json

rm -rf kodexa_cloud
mv .swagger_tmp/kodexa_cloud .
rm -r .swagger_tmp