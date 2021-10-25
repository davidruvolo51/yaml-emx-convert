#'////////////////////////////////////////////////////////////////////////////
#' FILE: index.py
#' AUTHOR: David Ruvolo
#' CREATED: 2021-09-07
#' MODIFIED: 2021-10-25
#' PURPOSE: example
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

# from emxconvert.convert import Convert
from src.emxconvert.convert import Convert

# set paths to YAML data models
c = Convert(files = ['dev/example/birddata.yaml'])

# convert model with defaults
c.convert()

# convert model by setting priority for a specific `name-` key
c.convert(priorityNameKey = 'name-projA')
c.convert(priorityNameKey = 'name-projB')
[print(d) for d in c.attributes[:3]]

# view results
c.packages
c.entities
c.attributes
c.data
c.tags

# write model to excel workbook
c.write(name = "birddata", format = 'xlsx', outDir = 'dev/example/model/')


# write model overview to file
c.write_schema(path = 'dev/example/model/birddata_schema.md')


#//////////////////////////////////////////////////////////////////////////////

# Run some basic tests
c = Convert(files = ['dev/example/birddata.yaml'])

# make sure fields are reset
def checkEmxStructure(num_pkgs = 1, num_entities = 4):
    """Check the model structure post-multiple builds
    Make sure the fields are properly reset
    
    Attributes:
            num_pkgs (int) : number of packages defined in the YAML file
        num_entities (int) : number of entities defined in the YAML file
    
    @returns status message
    """
    pkgTotal = []
    entityTotal = []
    for i in range(2):
        c.convert()
        pkgTotal.append(len(c.packages))
        entityTotal.append(len(c.entities))
    
    if not (list(set(pkgTotal)) == [num_pkgs]) or not (list(set(entityTotal)) == [num_entities]):
        raise ValueError(
            'Error in convert: fields are not properly reset (pkgs:{}, entities:{})'
            .format(pkgTotal, entityTotal)
        )
    else:
        print('EMX Structure properly resets each time')

checkEmxStructure(num_pkgs=1, num_entities=2)


# make sure priorityNameKey works properly
# def checkPriorityNameKey(entity: str = None, keysToCheck: list = []):

#     c.convert()
#     attr_def = c.attributes
#     attr_def_names = [d['name'] for d in attr_def if d['entity'] == entity]

#     for key in keysToCheck:
#         c.convert(priorityNameKey= key)
#         attr_set_names = [d['name'] for d in c.attributes if d['entity'] == entity]
#         count = [0 if not (name in attr_set_names) else 1 for name in attr_def_names]
#         if sum(count) > 0:
#             raise ValueError(
#                 'Error in key {}: not all priorityNameKeys are recoded properly'
#                 .format(key)
#             )
#         else:
#             print('PriorityNameKeys in {} are properly handled'.format(key))
            
# checkPriorityNameKey(entity = 'birdData_states' , keysToCheck = ['name-projA', 'name-projB'])
# checkPriorityNameKey(entity = 'birdData_species' , keysToCheck = ['name-species'])

        