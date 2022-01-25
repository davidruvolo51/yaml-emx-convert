from yamlemxconvert.convert import loadYaml


# mappings for molgenis/molgenis attributes to EMX2 attributes
__emx__to__emx2__ = {
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


__emx__datatypes__to__emx2__ = {
    # 'bool',
    'categorical': 'ref',
    'categorical_mref': 'ref_array',
    # 'compound',
    # 'date',
    # 'datetime',
    # 'decimal',
    'email': 'string',
    # 'enum',
    # 'file',
    'hyperlink': 'string',
    # 'int',
    'long': 'int',
    'mref': 'ref_array',
    'one_to_many': 'ref_array',
    # 'string',
    'text': 'string',
    'xref': 'ref'
}


class Convert2():
    
    def __init__(self, file: str = None):
        """Convert2
        Convert molgenis/molgenis YAML model to EMX2 format
        
        Attributes:
            files (list): a list of files to convert
        
        Examples:
            ```
            c = Convert2(files=['path/to/my/model'])
            ```
        """
        self.molgenis = []
    
    def convert(self):
        """Convert Model
        """
        self.molgenis = []
        print('Processing {}'.format(self.file))
        
        # yaml = loadYaml(file = self.file)
        yaml = loadYaml(file = 'dev/example/birddata.yaml')

        if 'entities' not in yaml:
            raise KeyError('Error: EMX entities are not defined in YAML')

        molgenis = []
        for entity in yaml['entities']:    

            if entity.get('attributes'):
                for row in entity.get('attributes'):

                    tmp = {'entity': entity.get('name')}
                 
                    for key in row.keys():
                        if key in __emx__to__emx2__:
                            value = row.get(key)
                            
                            # recode `idAttribute` to EMX2 `key`
                            if key == 'idAttribute':
                                print(key, value)
                                value = int(value == True)
                            
                            # apply model defaults
                            if (yaml.get('defaults')) and (key != 'idAttribute'):
                                if key in yaml.get('defaults'):
                                    value = yaml.get('defaults', {}).get(key)
                                    
                            # convert molgenis/molgenis `dataType` to EMX2 `columnType`
                            if key == 'dataType':
                                if value in __emx__datatypes__to__emx2__:
                                    value = __emx__datatypes__to__emx2__[value]
                                    

                            tmp[__emx__to__emx2__[key]] = value

                    molgenis.append(tmp)
            
                

# def convert2():
#     for entity in yaml['entities']:    
#         molgenis = []
#         if entity.get('attributes'):
#             for row in entity.get('attributes'):
#                 tmp = {'entity': entity.get('name')}
#                 for key in row.keys():
#                     if key in __emx__to__emx2__:
#                         value = row.get(key)
#                         if yaml.get('defaults'):
#                             if key in yaml.get('defaults'):
#                                 value = yaml.get('defaults', {}).get(key)
#                         if key == 'dataType':
#                             value = recodeAsEm2ColumnType(value)
#                         if key == 'idAttribute':
#                             print(key, value)
#                             value = int(value == 'True')
#                         tmp[__emx__to__emx2__[key]] = value
#                 molgenis.append(tmp)