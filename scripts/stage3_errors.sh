#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
for name in unknown_package no_test_file; do
    echo "== $name.yaml"
    python3 -m src.main "configs/errors/$name.yaml" graph 2>&1
done
