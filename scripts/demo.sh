#!/usr/bin/env bash
set -euo pipefail

pmflow doctor
pmflow demo

echo "Demo completed."
