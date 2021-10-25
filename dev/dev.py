#'////////////////////////////////////////////////////////////////////////////
#' FILE: dev.py
#' AUTHOR: David Ruvolo
#' CREATED: 2021-10-25
#' MODIFIED: 2021-10-25
#' PURPOSE: rename files for import into pypi
#' STATUS: working
#' PACKAGES: os, re
#' COMMENTS: files must be in the format: <package>_<username>_<version>.<ext>
#'////////////////////////////////////////////////////////////////////////////

import os
import re

# get version from __init__.py
with open('src/emxconvert/__init__.py', 'r') as stream:
    raw = [line for line in stream.readlines() if '__version__' in line][0]
    v = raw.split('=')[1].strip().replace('\'', '')
    stream.close()    

# rename files to fit pypi packaging guide
files = [ f'dist/{file}' for file in os.listdir('dist') ]
for file in files:
    file_basename = f'dist/emxconvert_dcruvolo_{v}'
    if re.search(r'(py3-none-any.whl)$', file):
        os.rename(file, f'{file_basename}-py3-none-any.whl')
    if re.search(r'(.tar.gz)$', file):
        os.rename(file, f'{file_basename}.tar.gz')

