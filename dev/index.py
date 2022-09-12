#///////////////////////////////////////////////////////////////////////////////
# FILE: index.py
# AUTHOR: David Ruvolo
# CREATED: 2022-09-12
# MODIFIED: 2022-09-12
# PURPOSE: local dev test script
# STATUS: in.progress
# PACKAGES: NA
# COMMENTS: NA
#///////////////////////////////////////////////////////////////////////////////

from yamlemxconvert.convert2 import Convert2

model = Convert2(file = 'tests/models/model_complex/birddata.yaml')
model.convert(keepModelPackage=True)

for row in model.model['molgenis']:
  if row.get('refSchema') == 'birdData_refs':
    row['refSchema'] = 'birdDataRefs'

refs = Convert2(file = 'tests/models/model_complex/birddata_refs.yaml')
refs.convert(keepModelPackage=False)
refs.model['molgenis']

refs.write(name="birdDataRefs",outDir='dev')
model.write(name="birdData",outDir='dev')
