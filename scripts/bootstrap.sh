#!/bin/bash
set -e -o pipefail



echo "⭐ Setup Nodejs "
# shellcheck source=/dev/null
# shellcheck disable=SC2086
[[ -s $HOME/.nvm/nvm.sh ]] && . "$HOME/.nvm/nvm.sh"  # Load NVM
nvm use

echo "⭐ Creating python virtual environment "
python3 -m venv .venv
# shellcheck disable=SC2086
# shellcheck source=/dev/null
source .venv/bin/activate
which python3
pip install pip-tools
pip-compile

echo "⭐ Installing tools"
pip install pep8
pip install flake8
pip install black
pip install pre-commit
pip install cfn-lint
pip install commitizen

echo "⭐ Installing requirements"
pip install -r requirements.txt

echo "⭐ Setup git "
git init
git remote add origin "http://www.github.com/cdk-all-the-things/cdk-python-pipeline"

echo "⭐ Initial Commit using Commitizen"
git add -A
git commit -m "feat(initial commit)"

make dev
