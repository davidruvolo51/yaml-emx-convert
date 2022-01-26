from multiprocessing.sharedctypes import Value
from yamlemxconvert.convert import loadYaml
from os import path, remove
import pandas as pd


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


# define mappings for all dataTypes (can change later)
__emx__datatypes__to__emx2__ = {
    'bool' : 'bool',
    'categorical': 'ref',
    'categorical_mref': 'ref_array',
    'compound': 'headings', # ???
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
    'one_to_many': 'ref_array',
    'string': 'string',
    'text' : 'text',
    'xref': 'ref'
}

class emxWriter2:
    def ___xlsx__headers__(self, wb, columns, name):
        """Write xlsx headers
        
        Attributes:
            wb: workbook object
            columns: a list of column names
            name: name of the sheet

        """
        sheet = wb.sheets[name]
        format = wb.book.add_format({'bold': False, 'border': False})
        for col, value in enumerate(columns):
            sheet.write(0, col, value, format)   
                
    def writeXlsx(self, model, path):
        """Write EMX as XLSX
        Attributes:
            model (obj) : converted EMX model
            path (str) : output file path
        """

        wb = pd.ExcelWriter(path = path, engine = 'xlsxwriter')
        
        for entity in model:
            df = pd.DataFrame(model[entity], index=range(0, len(model[entity])))
            df.to_excel(
                wb,
                sheet_name = entity,
                startrow = 1,
                header = False,
                index = False
            )
            self.___xlsx__headers__(wb, df.columns.values, entity)
            
        wb.save()


class Convert2():
    
    def __init__(self, file: str = None):
        """Convert2
        Convert molgenis/molgenis YAML model to EMX2 format
        
        Attributes:
            files (list): a list of files to convert
        
        Examples:
            ```
            c = Convert2(files='path/to/my/model.yaml')
            ```
        """
        self.file = file
        self.filename = self.file.split('/')[-1]
        self._yaml = loadYaml(file = self.file)
    
    def __data__to__emx2__(self, data: dict = {}, tablename: str = None):
        return {
            'tableName': tablename,
            'tableExtends': data.get('extends'),
            'columnName': data.get('name'),
            'columnType': data.get('dataType'),
            'key': data.get('idAttribute'),
            'required': data.get('nillable'),
            'refSchema': data.get('refEntity'),
            'refTable': data.get('refEntity'),
            'validation': data.get('validationExpression'),
            'semantics': data.get('tags'),
            'description': data.get('description')
        }
        
    def __refEntity__to__refSchema__(self, pkgName, value, flattenNestedPkgs):
        schema = value.split('_')[:-1]
        
        if flattenNestedPkgs:
            schema = schema[:1]
        
        try:
            schema.remove(pkgName)
        except ValueError:
            pass
        
        return schema if schema else None
    
            
    def __refEntity__to__refTable__(self, value):
        return value.split('_')[-1]

    
    def convert(self, includeData: bool = True, flattenNestedPkgs: bool = True):
        """Convert Model
        Convert molgenis/molgenis EMX-YAMl model format into EMX2
        
        Attributes:
            includeData (bool): If True (default), any datasets defined in the yaml
                will be written to file
            flattenNestedPkgs (bool) : If True (default), all nested EMX packages
                will be flattened so that the `refEntity` can be transformed into
                `refSchema`
            
        """
        print(f'Processing model: {self.filename}')
        self.model = {}

        if 'entities' not in self._yaml:
            raise KeyError('EMX entities are not defined in YAML')
            
        defaults = self._yaml.get('defaults')
        pkgName = self._yaml.get('name')
        molgenis = []

        for entity in self._yaml['entities']:            
            entityName = entity.get('name')
            entityMeta = self.__data__to__emx2__(
                data = entity,
                tablename = entityName
            )
            
            # recode `tableExtends`
            if entityMeta.get('tableExtends'):
                entityMeta['tableExtends'] = self.__refEntity__to__refTable__(
                    value = entityMeta.get('tableExtends')
                )
            
            molgenis.append(entityMeta)

            # build data for `molgenis` worksheet
            if entity.get('attributes'):
                for attr in entity.get('attributes'):
                    attrData = self.__data__to__emx2__(
                        data = attr,
                        tablename = entityName
                    )
                    
                    # recode `dataType` to `columnType`
                    if (not attrData.get('columnType')) and defaults.get('dataType'):
                        attrData['columnType'] = defaults.get('dataType')
                    
                    if (not attrData.get('columnType')) and (not defaults.get('dataType')):
                        attrData['columnType'] = 'string'
                        
                    attrData['columnType'] = __emx__datatypes__to__emx2__[
                        attrData['columnType']
                    ]
                        
                    # recode `idAttribute` to `key`
                    if attrData.get('key'):
                        attrData['key'] = int(attrData['key'] == True)
                        
                    # recode `refEntity` as `refSchema`
                    if attrData.get('refSchema'):
                        attrData['refSchema'] = self.__refEntity__to__refSchema__(
                            pkgName = pkgName,
                            value = attrData.get('refSchema'),
                            flattenNestedPkgs = flattenNestedPkgs
                        )
                    
                    # recode `refEntity` as `refTable`
                    if attrData.get('refTable'):
                        attrData['refTable'] = self.__refEntity__to__refTable__(
                            value = attrData.get('refTable')
                        )
                    
                    molgenis.append(attrData)

            self.model['molgenis'] = molgenis

            # extract data if defined in the YAML file                  
            if (includeData) and (entity.get('data')):
                self.model[entityName] = entity.get('data')
            
    def write(
        self,
        name: str = None,
        format: str = 'xlsx',
        outDir: str = '.'
    ):
        """Write EMX to XLSX
        Write EMX2 model to file
        
        Attributes:
            name (str) : name of the model
            outDir (str) : directory to save the file(s). The default is the
                current directory i.e. '.'
        """
        
        if not name:
            raise ValueError('value for name cannot be `None`')
        
        if format not in ['csv','xlsx']:
            raise ValueError(f'Invalid format {str(format)}. Use csv or xlsx')
        
        writer = emxWriter2()
        
        if format == 'xlsx':
            file = f'{outDir}/{name}.{str(format)}'
            if path.exists(file):
                remove(file)
            writer.writeXlsx(model = self.model, path = file)
          
        # not yet implemented!!  
        # if format == 'csv':
        #     dir = getcwd() if outDir == '.' else path.abspath(outDir)
        #     if not path.exists(dir):
        #         raise ValueError(f'Path {dir} does not exist')
            
        #     writer.writeCsv(model = self.model, dir = dir)
