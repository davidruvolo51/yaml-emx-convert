#'////////////////////////////////////////////////////////////////////////////
#' FILE: index.py
#' AUTHOR: David Ruvolo
#' CREATED: 2021-09-07
#' MODIFIED: 2021-09-20
#' PURPOSE: test conversion
#' STATUS: working
#' PACKAGES: NA
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

from emxconvert.convert import Convert
# from src.emxconvert.convert import Convert

# set paths to YAML data models
c = Convert(files = [
    'dev/example/mypkg.yaml',
    'dev/example/birddata.yml', 
    'dev/example/birddata_refs.yaml'
])

# convert model with defaults
c.convert()

# convert model by setting priority for a specific `name-` key
c.convert(priorityNameKey = 'name-species')


# view results
c.packages
c.entities
c.attributes
c.data


# write model to excel workbook
c.write(name = "birddata", format = 'xlsx', outDir = 'dev/example/model/')


# write model overview to file
c.write_schema(path = 'dev/example/model/birddata_schema.md')