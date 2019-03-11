#!/bin/bash
set -eu

echo "start run pytest."

pytest -v -s testcases/

echo "pytest done."

set +eu