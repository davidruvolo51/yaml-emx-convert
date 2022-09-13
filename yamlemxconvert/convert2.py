from os import path, getcwd, remove
from yamlemxconvert.utils import loadYaml
from yamlemxconvert.emxWriter import emxWriter2
from yamlemxconvert.mappings import __emx__datatypes__to__emx2__
    
class Convert2():
  def __init__(self, file: str = None):
    """Convert2
    Convert molgenis/molgenis YAML model to EMX2 format
    
    @param file a location to the yaml-emx model
    
    Examples:
        ```
        from yamlemxconvert.convert import Convert2
        c = Convert2(file = 'path/to/my/model.yaml')
        ```
    """
    self.file = file
    self.filename = self.file.split('/')[-1]
    self._yaml = loadYaml(file = self.file)
    self.name = None
    self.date = None
    self.version = None
  
  def __data__to__emx2__(self, data: dict = {}, tablename: str = None):
    """Map molgenis/molgenis to EMX2
    Pull data from EMX1 model and map to EMX2 attributes
    
    @param data a dict in entity['attributes']
    @param tablename name of the entity that `data` is associated with (i.e., entity name)
    """
    return {
      'tableName': tablename,
      'tableExtends': data.get('extends'),
      'columnName': data.get('name'),
      'columnType': data.get('dataType'),
      'key': data.get('idAttribute'),
      'required': not data['nillable'] if data.get('nillable') is not None else None,
      'refSchema': data.get('refEntity'),
      'refTable': data.get('refEntity'),
      'validation': data.get('validationExpression'),
      'semantics': data.get('tags'),
      'description': data.get('description')
    }
      
  def __refEntity__to__refSchema__(
    self,
    value: str = None,
    keepModelPackage: bool = False
  ):
    """Convert refEntity to refSchema
    If applicable, split the refEntity value and extract value for refSchema
    
    @param value refEntity value
    @param keepModelPackage If True, the EMX1 package name will be
      returned as is. This is useful when the models are stored separately or
      you would like to restructure the EMX1 instance. Remember to modify the
      schema names afterwards if required.
    """
    return '_'.join(value.split('_')[:-1]) if keepModelPackage else None
  
  def __refEntity__to__refTable__(self, value: str = None):
    """RefEntity to RefTable
    Extract the table name from RefEntity
    
    Attributes:
        value (str) : value for refEntity
    """
    return value.split('_')[-1]
  
  def convert(self, includeData: bool = True, keepModelPackage: bool = False):
    """Convert Model
    Convert molgenis/molgenis EMX-YAMl model format into EMX2
    
    @param includeData (bool): If True (default), any datasets defined in the yaml
      will be written to file
    @param keepModelPackage If True, the EMX1 package name will be
      returned as is. This is useful when the models are stored separately or
      you would like to restructure the EMX1 instance. Remember to modify the
      schema names afterwards if required.
    """
    print(f'Processing model: {self.filename}')
    self.model = {}

    if 'entities' not in self._yaml:
      raise KeyError('EMX entities are not defined in YAML')
      
    if keepModelPackage:
      print('Warning: All ref attributes will keep the EMX1 format. Make sure these are changed before importing into EMX2.')

    defaults = self._yaml.get('defaults')
    self.name = self._yaml.get('name')
    molgenis = []

    for entity in self._yaml['entities']:            
      entityName = entity.get('name')
      entityMeta = self.__data__to__emx2__(data = entity, tablename = entityName)
      entityMeta['columnName'] = None
        
      # recode `tableExtends`
      if entityMeta.get('tableExtends'):
        entityMeta['tableExtends'] = self.__refEntity__to__refTable__(value = entityMeta.get('tableExtends'))
        
      molgenis.append(entityMeta)

      # build data for `molgenis` worksheet
      if entity.get('attributes'):
        for attr in entity.get('attributes'):
          attrData = self.__data__to__emx2__(data = attr, tablename = entityName)
            
          # assign YAML default if defined
          if (not attrData.get('columnType')) and defaults.get('dataType'):
            attrData['columnType'] = defaults.get('dataType')
          
          # assign 'string' as default if applicable
          if (not attrData.get('columnType')) and (not defaults.get('dataType')):
            attrData['columnType'] = 'string'
              
          # blanket recode of all `dataType` values into `columnType`
          attrData['columnType'] = __emx__datatypes__to__emx2__[attrData['columnType']]
              
          # recode `idAttribute` to `key`
          if attrData.get('key'):
            attrData['key'] = int(attrData['key'] == True)
              
          # recode `refEntity` as `refSchema`
          if attrData.get('refSchema'):
            attrData['refSchema'] = self.__refEntity__to__refSchema__(
              value = attrData.get('refSchema'),
              keepModelPackage = keepModelPackage
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
          
  def write(self,name: str = None,format: str = 'xlsx',outDir: str = '.'):
    """Write EMX to XLSX
    Write EMX2 model to file
    
    @param name name of the model
    @param outDir directory to save the file(s). The default is the current directory i.e. '.'
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
    if format == 'csv':
      dir = getcwd() if outDir == '.' else str(outDir)
      writer.writeCsv(model = self.model, dir = dir)
