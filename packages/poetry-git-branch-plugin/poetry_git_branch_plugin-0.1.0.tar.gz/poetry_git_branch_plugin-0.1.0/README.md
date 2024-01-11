# Poetry Git Branch Plugin
A simple poetry plugin that sets an environment variable containing the name of the current checked-out branch before executing any poetry command.

## Why
Our main use case is in situations where DBT needs access to the current git branch name to set the name of the target schema.

## Installation
The plugin cannot be installed with `poetry self add` because it is not published on PyPI.
Instead, you can install it by building a wheels file
```bash
poetry build
```
and installing it with your system-wide or pyenv-wide pip.
```bash
# not inside pycharm nor inside a poetry shell
pip install /path/to/poetry-git-branch-plugin/dist/poetry_git_branch_plugin-0.1.0-py3-none-any.whl
```
