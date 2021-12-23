#!/bin/bash -eu
SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd ${SCRIPT_DIR}

APP_NAME=sample-cdk

docker run \
  --rm \
  -it \
  -v ${PWD}:/opt/cdk \
  -v ${HOME}/.aws:/root/.aws:ro \
  ${APP_NAME} cdk $*
