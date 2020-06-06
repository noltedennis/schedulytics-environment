#!/usr/bin/env python3

"""
kustomize.py
This script is designed to be used as environment-independant
post-renderer for Helm. It will take stdin and include it in its
kustomize build of the relative directory kustomize/${BUILDTARGET}.
In addition, it will order certain resource kinds to be created first,
because kustomize currently lacks inter-dependency ordering.

Required inputs:
  STDIN       - Output from Helm template
  BUILDTARGET - Environment variable, one of "local" or "prod"

Output:
  STDOUT      - A resource definition run through kustomize & custom
                ordering

Requires:
  - Local installation of kustomize (in PATH)
  - Python 3.6 or higher
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
with open(helm_out, 'wb') as text_file:
    content = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8').read()
    text_file.write(content.encode('utf-8'))

# Execute kustomize on that and store result
kustomize_out = subprocess.check_output(['kubectl', 'kustomize', str(kustomize_dir)], shell=True)

# Read results and output them according to priorization
ordered_kinds = ['CustomResourceDefinition' 'ValidatingWebhookConfiguration']

for x in yaml.load_all(yaml.load(kustomize_out, Loader=yaml.FullLoader)):
    if x['kind'] in ordered_kinds:
      print('---')
      print(yaml.dump(x,encoding=('utf-8')))

for x in yaml.load_all(kustomize_out):
    if x['kind'] not in ordered_kinds:
      print('---')
      print(yaml.dump(x,encoding=('utf-8')))

# Cleanup
os.remove(helm_out)