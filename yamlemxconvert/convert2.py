from yamlemxconvert.convert import emxWriter, loadYaml
from os import path, remove
import pandas as pd

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


# TODO: double check mappings, especially ref mappings
__emx__datatypes__to__emx2__ = {
    # 'bool',
    'categorical': 'ref',
    'categorical_mref': 'ref_array',
    # 'compound': 'headings', # ???
    # 'date',
    # 'datetime',
    # 'decimal',
    'email': 'string', # temporary mapping
    # 'enum',
    # 'file',
    'hyperlink': 'string', # temporary mapping
    # 'int',
    'long': 'int',  # use `int` for now
    'mref': 'ref_array',
    'one_to_many': 'ref_array',
    # 'string',
    # 'text',
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
            c = Convert2(files=['path/to/my/model'])
            ```
        """
        self.__init__fields__()

        self._yaml = loadYaml(file = self.file)
        self.filename = file.split('/')[-1]
        
    def __init__fields__(self):
        self._yaml = []
        self.model = {}
        self.filename = None
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # CONVERT
    # `convert` is the primary method for converting a YAML-EMX model into a
    # Molgenis EMX2 file(s). This is sort of an extension of the
    # molgenis/molgenis converter that allows models to also be rendered for
    # the new version of Molgenis. Not all features from the regular `Convert`
    # class have been integrated as this is sort of experimental, and the
    # primary purpose is to have a *quick* converter so that we don't have
    # to manually maintain more than one model.
    def convert(self):
        """Convert Model
        Convert molgenis/molgenis EMX-YAMl model format into EMX2
            
        """
        print(f'Processing model: {self.filename}')
        self.__init__fields__()

        if 'entities' not in self._yaml:
            raise KeyError('Error: EMX entities are not defined in YAML')
            
        if 'defaults' in self.__yaml:
            defaults = self._yaml.get('defaults')

        molgenis = []
        for entity in self._yaml['entities']:
            
            entityName = entity.get('name')    

            # build data for `molgenis` worksheet
            if entity.get('attributes'):
                for row in entity.get('attributes'):
                    tmp = {'entity': entityName}
                 
                    for key in row.keys():
                        if key in __emx__to__emx2__:
                            value = row.get(key)
                            
                            # recode `idAttribute` to `key`
                            if key == 'idAttribute':
                                value = int(value == True)
                            
                            # apply YAML defaults
                            if (defaults) and (key != 'idAttribute'):
                                if key in defaults:
                                    value = defaults.get(key)
                                    
                            # recode `dataType` to `columnType`
                            if key == 'dataType':
                                if value in __emx__datatypes__to__emx2__:
                                    value = __emx__datatypes__to__emx2__[value]

                            tmp[__emx__to__emx2__[key]] = value

                    molgenis.append(tmp)
            self.model['molgenis'] = molgenis

            # extract data if defined                    
            if entity.get('data'):
                self.model[entityName] = entity.get('data')
            
    def write(
        self,
        name: str = None,
        format: str = 'xlsx',
        outDir: str = '.',
        includeData: bool = True
    ):
        """Write EMX to XLSX
        Write EMX2 model to file
        
        Attributes:
            name (str) : name of the model
            outDir (str) : directory to save the file(s). The default is the
                current directory i.e. '.'
            includeData (bool) : if True (default), all datasets defined in
                the yaml will be written to file
        """
        
        if format not in ['csv','xlsx']:
            raise ValueError(f'Invalid format {str(format)}. Use csv or xlsx')
        
        writer = emxWriter2()
        
        if format == 'xlsx':
            file = f'{outDir}/{name}.{str(format)}'
            if path.exists(file):
                remove(file)
            