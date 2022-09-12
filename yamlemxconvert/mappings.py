#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EMX Attributes
# Define lists of known EMX attributes. This lists will be used to identify
# and extract the contents YAML file, as well as offer some sort of pre-import
# validation.
# 
# The metadata below was pulled from the documentation:
# https://molgenis.gitbook.io/molgenis/data-management/guide-emx#attributes-options
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__emx__keys__pkgs__ = ['name', 'label', 'description', 'parent', 'tags']
__emx__keys__enty__ = [
  'name',
  'label',
  'extends',
  'package',
  'abstract',
  'description',
  'backend',
  'tags'
]
__emx__keys__attr__ = [
  'entity',
  'name',
  'dataType',
  'refEntity',
  'nillable',
  'idAttribute',
  'auto',
  'description',
  'rangeMin',
  'rangeMax',
  'lookupAttribute',
  'label',
  'aggregateable',
  'labelAttribute',
  'readOnly',
  'tags',
  'validationExpression',
  'visible',
  'defaultValue',
  'partOfAttribute',
  'expression',
  'enumOptions'
]

__emx__keys__datatype__ = [
  'bool',
  'categorical',
  'categorical_mref',
  'compound',
  'date',
  'datetime',
  'decimal',
  'email',
  'enum',
  'file',
  'hyperlink',
  'int',
  'long',
  'mref',
  'one_to_many',
  'string',
  'text',
  'xref'
]

__emx__keys__tags__ = [
  'identifier',
  'label',
  'objectIRI',
  'relationLabel',
  'relationIRI',
  'codeSystem'
]

# @name __emx__attribs__to__emx
# @description mappings for attribute names
# @reference https://github.com/molgenis/molgenis-emx2/blob/master/backend/molgenis-emx2/src/main/java/org/molgenis/emx2/Column.java
__emx__attribs__to__emx2__ = {
  # 'entity': 'tableName', # processed in convert2 method
  'extends': 'tableExtends', 
  'name': 'name', 
  'dataType': 'columnType', 
  'idAttribute': 'key', 
  'nillable': 'required', 
  'refEntity': 'refSchema', 
  'refEntity': 'refTable', 
  # '': 'refLink', # no matching molgenis/molgenis type
  # '': 'refBack', # no matching molgenis/molgenis type
  'validationExpression': 'validation', 
  'tags': 'semantics',
  'description': 'description'
}


# @name __emx__datatypes__to__emx__
# @description mapping dataTypes to columnTypes
# @reference https://github.com/molgenis/molgenis-emx2/blob/master/backend/molgenis-emx2/src/main/java/org/molgenis/emx2/ColumnType.java
__emx__datatypes__to__emx2__ = {
  'bool' : 'bool',
  'categorical': 'ref', # TBD: ontology
  'categorical_mref': 'ref_array', # TBD: ontology_array
  'compound': 'heading', # ???
  'date' : 'date',
  'datetime' : 'datetime',
  'decimal' : 'decimal',
  'email': 'string', # temporary mapping
  'enum': None, # temporary mapping
  'file' : 'file',
  'hyperlink': 'string', # temporary mapping
  'int': 'int',
  'long': 'int',  # use `int` for now
  'mref': 'ref_array',
  'one_to_many': 'refback', # process mappedBy
  'string': 'string',
  'text' : 'text',
  'xref': 'ref'
}
