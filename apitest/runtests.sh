#!/bin/bash
set -eu

echo "[PYTEST] start run api test."
cd ${HOME}/Workspaces/zj_py3_project/apitest 
# run test_base.py first to init env and load data
pytest -v -s testcases/test_base.py testcases/ --alluredir outputs/results/

echo "[PYTEST] generate allure report."
allure generate outputs/results/ -o outputs/reports/ --clean

echo "[PYTEST] api test done."

set +eu
