#!/bin/bash

if [ -z "$FC_DEMO_IMAGE" ]
then
  echo "Argument image is required but not provided. Usage: $0 acr-image-name;"
  exit 1
fi

perl -i -p -e 's/{FC_DEMO_IMAGE}/$ENV{"FC_DEMO_IMAGE"}/g' ./template.yml
