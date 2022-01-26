#'////////////////////////////////////////////////////////////////////////////
#' FILE: index.py
#' AUTHOR: David Ruvolo
#' CREATED: 2022-01-26
#' MODIFIED: 2022-01-26
#' PURPOSE: dev test script for EMX2 conversion tests
#' STATUS: experimental
#' PACKAGES: **see below**
#' COMMENTS: NA
#'////////////////////////////////////////////////////////////////////////////

# install package first
# use one of the following commands
#
# ```
# tox -e build 
# python setup.py sdist
# python setup.py bdist_wheel
# ```

# from emxconvert.convert2 import Convert2
from yamlemxconvert.convert2 import Convert2
c = Convert2(file = 'dev/example-emx2/index.yaml')
c.convert(includeData=False)

c.model['molgenis']

c.write(name='yaml_emx2', outDir = 'dev/example-emx2/')