#!/bin/bash -eu
PROJECT_ROOT=$(cd $(dirname $0); pwd)
cd ${PROJECT_ROOT}

IMAGE_NAME=$(cat ${PROJECT_ROOT}/cdk_image_name)

docker run \
  --rm \
  -it \
  -v ${PWD}:/opt/cdk \
  -v ${HOME}/.aws:/root/.aws:ro \
  ${IMAGE_NAME} cdk $*
