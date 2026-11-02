#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
for name in simple cycle deep; do
    echo "== $name.yaml"
    python3 -m src.main "configs/$name.yaml" order
done
