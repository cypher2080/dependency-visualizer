#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
for name in missing no_package no_repository bad_mode bad_depth zero_depth unknown_key; do
    echo "== $name.yaml"
    python3 -m src.main "configs/errors/$name.yaml" params 2>&1
done
