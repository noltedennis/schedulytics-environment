#!/bin/bash

############################################################################
# This script invokes kustomize as a a post-renderer.
#
# Usage:
#   STDIN | kustomize.sh
#
#  ToDos:
#    - Change to python for cross-compatibility
#    - Try to reorder CRDs (https://github.com/Agilicus/kustomize-plugins/tree/master/agilicus/v1/crdgenerator, https://github.com/kubernetes-sigs/kustomize/issues/821)
#
# Required environment configuration:
#   BUILDTARGET         either "local" or "PROD"
############################################################################

# Runtime information, base everything on caller directory
DIR=$(pwd)

if [ -z ${BUILDTARGET} ]; then
  echo "Variable BUILDTARGET must be defined"
  exit 1;
fi

KUSTOMIZE_DIR=${DIR}/kustomize/${BUILDTARGET}

cat <&0 > ${KUSTOMIZE_DIR}/all.yaml

kubectl kustomize ${KUSTOMIZE_DIR}