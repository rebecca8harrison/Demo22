#!/bin/bash

set -euo pipefail

pipenv run python -m unittest python/testing/test_buggy.py