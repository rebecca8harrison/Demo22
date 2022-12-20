#!/bin/bash

set -euo pipefail

pipenv run python -m doctest python/testing/buggy_doctests.py