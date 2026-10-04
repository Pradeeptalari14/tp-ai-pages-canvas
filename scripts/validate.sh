#!/usr/bin/env bash
set -euo pipefail

echo "=================================================="
echo " Validating Pages Dynamic Canvas Engine"
echo "=================================================="

python3 -m py_compile canvas_reactive_kernel.py
python3 -m py_compile dag_dependency_resolver.py

python3 canvas_reactive_kernel.py
python3 dag_dependency_resolver.py

echo "Validation successful!"
