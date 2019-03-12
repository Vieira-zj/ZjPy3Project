#!/bin/bash
set -u

echo "start run pytest."
cd ${HOME}/Workspaces/zj_py3_project/pytests 
#pytest -v -s test_pytest.py --alluredir output/results/
pytest -v -s ./ --alluredir output/results/

echo "generate allure report."
allure generate output/results/ -o output/reports/ --clean

echo "pytest done."

set +u
