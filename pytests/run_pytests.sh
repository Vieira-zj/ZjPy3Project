#!/bin/bash
set -eu

echo "start run pytest."
cd /Users/zhengjin/Workspaces/zj_py3_project/pytests
pytest -v -s test_pytest.py --alluredir output/results/

echo "generate allure report."
allure generate output/results/ -o output/reports/ --clean

echo "pytest done."

set +eu
