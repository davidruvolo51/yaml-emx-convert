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

from yamlemxconvert.convert import Convert2
# from yamlemxconvert.convert2 import Convert2
c = Convert2(file = 'dev/example-emx2/index.yaml')
c.convert()

c.model['molgenis']

c.write(name='yaml_emx2', outDir = 'dev/example-emx2/')


#//////////////////////////////////////

# ~ 2 ~
# Alternative Tests

from yamlemxconvert.convert import Convert
from yamlemxconvert.convert import Convert2

file = 'dev/example-emx1/birddata.yaml'
emx1 = Convert(files =[file])
emx2 = Convert2(file = file)

emx1.convert()
emx2.convert()

emx1.write(name='birddata_emx1', format='xlsx', outDir='~/Desktop/')
emx2.write(name='birddata_emx2', format='xlsx', outDir = '~/Desktop/')