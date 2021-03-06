#!/usr/bin/env python3

"""
kustomize.py
This script is designed to be used as environment-independant
post-renderer for Helm. It will take stdin and include it in its
kustomize build of the relative directory kustomize/${BUILDTARGET}.

Required inputs:
  STDIN       - Output from Helm template
  BUILDTARGET - Environment variable, one of "local" or "prod"

Output:
  STDOUT      - A resource definition run through kustomize & custom
                ordering

Requires:
  - Local installation of kustomize (in PATH)
  - Python 3.5 or higher
  - PyYAML
"""

import io
import os
import subprocess
import sys
import yaml

from pathlib import Path

# Read environment variable for environment
build_target = os.getenv('BUILDTARGET')
if build_target != 'local' and build_target != 'prod':
    print("Environment variable BUILDTARGET must be set to either 'local' or 'prod'")
    sys.exit(1)
kustomize_dir = Path('kustomize', build_target)

# Read stdin and write to file
helm_out = str(kustomize_dir / 'all.yaml')
with io.open(helm_out, 'w', encoding='utf8') as text_file:
    helm_template = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8').read()
    text_file.write(helm_template)

# Execute kustomize on that and store result
kustomize_out = subprocess.check_output('kubectl kustomize ' + str(kustomize_dir), shell=True)

# Read results and output them
for x in yaml.load_all(kustomize_out, Loader=yaml.FullLoader):
    print('---')
    print(yaml.dump(x))

# Cleanup
os.remove(helm_out)