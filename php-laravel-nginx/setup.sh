#!/bin/bash

if [ -z "$FC_DEMO_IMAGE" ]
then
  echo "Argument image is required but not provided. Usage: $0 acr-image-name;"
  exit 1
fi

if [ -z "$FC_ACCOUNT" ]
then
  echo "Argument account is required but not provided. Usage: $1 account ID;"
  exit 1
fi

perl -i -p -e 's/{FC_DEMO_IMAGE}/$ENV{"FC_DEMO_IMAGE"}/g' s.yaml
perl -i -p -e 's/{FC_ACCOUNT}/$ENV{"FC_ACCOUNT"}/g' s.yaml