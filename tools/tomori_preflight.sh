#!/bin/bash

set -e

echo "[TOMORI PREFLIGHT]"

pwd
ls -la

if [ -n "$1" ]; then
  if [ ! -e "$1" ]; then
    echo "STOP: path not found -> $1"
    exit 1
  else
    echo "OK: path exists -> $1"
  fi
fi

echo "Preflight OK"
