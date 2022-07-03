#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0); pwd)
PROJECT_ROOT=$(cd $(dirname $0)/..; pwd)
cd $PROJECT_ROOT
pytest tests