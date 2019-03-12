#!/bin/bash
set -u

echo "start run pytest."
cd ${HOME}/Workspaces/zj_py3_project/pytests 
#pytest -v -s test_pytest.py --alluredir outputs/results/
#pytest -v -s ./ --alluredir outputs/results/

# run test_base first to init env.
pytest -v -s ./test_pytest_base.py ./ --alluredir outputs/results/

echo "generate allure report."
allure generate outputs/results/ -o outputs/reports/ --clean

echo "pytest done."

set +u
