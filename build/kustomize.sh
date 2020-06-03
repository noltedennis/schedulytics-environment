#!/bin/bash

############################################################################
# This script invokes kustomize as a a post-renderer.
#
# Usage:
#   STDIN | kustomize.sh
#
# Required environment configuration:
#   BUILDTARGET         either "local" or "PROD"
############################################################################

# Runtime information
DIR=$(dirname $0)


if [ -z ${BUILDTARGET} ]; then
  echo "Variable BUILDTARGET must be defined"
  exit 1;
fi

KUSTOMIZE_DIR=${DIR}/${BUILDTARGET}

cat <&0 > ${KUSTOMIZE_DIR}/all.yaml

kubectl kustomize ${KUSTOMIZE_DIR}

rm ${KUSTOMIZE_DIR}/all.yaml