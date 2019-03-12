#!/bin/bash
set -eu

echo "[PYTEST] start run api test."
cd ${HOME}/Workspaces/zj_py3_project/apitest 
# run test_base.py first to init env and load data
pytest -v -s testcases/test_base.py testcases/ --alluredir outputs/results/

# run logs options
#-vv -o log_cli=true -o log_cli_level=INFO --log-date-format="%Y-%m-%d %H:%M:%S" --log-format="%(filename)s:%(lineno)s %(asctime)s %(levelname)s %(message)s"

echo "[PYTEST] generate allure report."
allure generate outputs/results/ -o outputs/reports/ --clean
# outputs: logs/, results/, reports/

echo "[PYTEST] api test done."

set +eu
