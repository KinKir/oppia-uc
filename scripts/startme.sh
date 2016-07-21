#!/usr/bin/env bash

if [ -z "$BASH_VERSION" ]
then
  echo ""
  echo "    Please run me using bash: "
  echo ""
  echo "         bash $0"
  echo ""
  return 1
fi

bash scripts/start.sh --save_datastore
