#!/bin/bash
PROJECT_ROOT=$(cd $(dirname $0)/..; pwd)
cd ${PROJECT_ROOT}
pyreverse -o png -d ./doc/image --colorized --max-color-depth=3 -p cdk .