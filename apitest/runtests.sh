#!/bin/bash
set -eu

echo "start run api test."
cd ${HOME}/Workspaces/zj_py3_project/apitest 
# run test_base.py first to init env and load data
pytest -v -s testcases/test_base.py testcases/ --alluredir outputs/results/

echo "generate allure report."
allure generate outputs/results/ -o outputs/reports/ --clean

echo "api test done."

set +eu
