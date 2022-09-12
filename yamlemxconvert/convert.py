from os import path, getcwd, remove
from yamlemxconvert.utils import loadYaml
from yamlemxconvert.markdownWriter import markdownWriter
from yamlemxconvert.emxWriter import emxWriter
from yamlemxconvert.mappings import (
  __emx__keys__pkgs__,
  __emx__keys__enty__,
  __emx__keys__attr__,
  __emx__keys__datatype__,
  __emx__keys__tags__
)

class Convert:
  def __init__(self, files: list = []):
    """Convert
    Read and transform a YAML-EMX markup into excel (CSV, xlsx) EMX format

    @param files (list): a list of files to convert
    @examples
    ```
    c = Convert(files = ['path/to/my_model.yml', 'path/to/my_model_1.yml'])
    ```
    """
    self.files = files
    self.name = None
    self.__init__fields__()
  
  def __init__fields__(self):
    self.packages = []
    self.entities = []
    self.attributes = []
    self.tags = []
    self.data = {}
    self.date = None,
    self.version = None
    self.priorityNameKey = None
    self.lang_attrs = ('label-', 'description-')
  
  def __emx__extract__package__(self, data, includePkgMeta: bool = True):
    """Extract EMX Package Metadata
    Extract known EMX package attributes
    
    @param data (list): contents of a yaml file
    @param includePkgMeta (bool): if TRUE (default), version and date will
      be added to description
    """
    pkg = {}
    keys = list(data.keys())
    for k in keys:
      if k in __emx__keys__pkgs__ or k.startswith(self.lang_attrs):
        pkg[k] = data[k]
    
    if includePkgMeta:
      pkgMeta = {}
      if 'version' in keys:
        pkgMeta['version'] = "v" + str(data['version'])
        self.version = str(data['version'])
      if 'date' in keys:
        pkgMeta['date'] = str(data['date'])
        self.date = str(data['date'])
      if pkgMeta:
        if 'description' in keys:
          pkg['description'] = pkg['description'] + '(' + ', '.join(pkgMeta.values()) + ')'
        else:
          pkg['description'] = '; '.join(pkgMeta.values())
    return pkg

  def __emx__extract__tags__(self, tags):
    """Extract known EMX tags

    @param tags (list) : if present, a list of dictionaries containing
      tag definitions. Properties must be defined under the `tagDefinitions` tag.
    """
    for tag in tags:
      keys = list(tag.keys())
      for k in keys:
        if not (k in __emx__keys__tags__):
          del tag[k]
    return tags                    

  def __emx__extract__entities__(self, data):
    """Extract known EMX entity attributes
    
    @param data (list): contents of a yaml file
    """
    emx = {'entities': [], 'attributes': [], 'data': {}}
    for entity in data['entities']:
      entityKeys = list(entity.keys())
      if 'name' not in entityKeys:
        raise ValueError('Error in entity: missing required attribute "name"')

      # pull entity info
      e = {'package': data['name']}
      for ekey in entityKeys:
        if ekey in __emx__keys__enty__ or ekey.startswith(self.lang_attrs):
          e[ekey] = entity[ekey]
      emx['entities'].append(e)

      # pull attribute definitions
      if 'attributes' in entity:
        attributes = entity['attributes']
        for attr in attributes:
          attrKeys = list(attr.keys())
          d = {'entity': data['name'] + '_' + entity['name']}
          for aKey in attrKeys:
            if aKey in __emx__keys__attr__ or aKey.startswith(self.lang_attrs) or aKey == self.priorityNameKey:
              d[aKey] = attr[aKey]
                  
          # adjust priorityKey if mulitple `name` attributes are used
          if bool(self.priorityNameKey):
            if (self.priorityNameKey in d) and (d[self.priorityNameKey] != 'none'):
              d.pop('name')
              d['name'] = d.get(self.priorityNameKey)
              d.pop(self.priorityNameKey)

          # provide dataType validation
          if 'dataType' in d:
            if d['dataType'] not in __emx__keys__datatype__:
              raise ValueError(
                'Error in Convert: for the attribute',
                d['name'],'in entity,',d['entity'],'dataType "', d['dataType'],'"',
                'is invalid.'
              )

          # apply defaults
          if data['defaults']:
            defaultKeys = list(data['defaults'].keys())
            for dKey in defaultKeys:
              if dKey not in attrKeys:
                d[dKey] = data['defaults'][dKey]

          emx['attributes'].append(d)

      if 'data' in entity:
        name = data['name'] + '_' + entity['name']
        emx['data'][name] = entity['data']

    return emx
  
  def convert(self, includePkgMeta: bool = True, priorityNameKey: str = None):
    """Convert Model
    Convert one or more yaml files into EMX structure. The contents of the
    yaml-emx markup will produce several data objects: packages, entities,
    attributes, data, and tags.
    
    @param includePkgMeta (bool): if TRUE (default), version and date will
      be added to description if defined in the yaml
    @param priorityNameKey (str): For EMX markups that are harmonization
      projects (i.e., multiple `name` attributes), you can set
      which name attribute gets priority. This means that you can
      compile the EMX for different projects.
    """
    self.__init__fields__()
    if priorityNameKey:
      self.priorityNameKey = priorityNameKey
    
    for file in self.files:
      print('Processing: {}'.format(file))
      yaml = loadYaml(file)
  
      keys = list(yaml.keys())
      if ('name' not in keys) and ('include' not in keys):
        raise ValueError('Error in convert: missing required attribute "name"')
      self.name = yaml['name']
      
      # Is the package defined by an another file?
      # Build self.emx['package'] based on the presence of 'include'. This option
      # is useful for situations where a package may have multiple subpackages or
      # if there are entities that are defined in multiple files.
      if 'include' in keys:
        include_yaml = loadYaml(yaml['include'])
        pkg = self.__emx__extract__package__(include_yaml, includePkgMeta)
        if pkg['name'] not in [d['name'] for d in self.packages]:
          self.packages.append(pkg)
        yaml.update(pkg)
      else:
        self.packages.append(self.__emx__extract__package__(yaml, includePkgMeta))
          
      # Are there tags?
      # If the object 'tagDefinitions' is present, append to self.tags
      if 'tagDefinitions' in keys:
        tags = self.__emx__extract__tags__(yaml['tagDefinitions'])
        self.tags.extend(tags)
      
      # process all entities and attributes
      emx = {}        
      if 'entities' in keys:
        emx = {**self.__emx__extract__entities__(yaml)}

      # append EMX components to model where applicable
      if 'entities' in emx: self.entities.extend(emx['entities'])
      if 'attributes' in emx: self.attributes.extend(emx['attributes'])
      if 'data' in emx: self.data.update(emx['data'])

  def write(
      self,
      name: str = None,
      format: str = 'xlsx',
      outDir: str = '.',
      includeData: bool = True
  ):
    """Write EMX to csv or xlsx
    Write the EMX model to file as csv or xlsx. If excel workbook format is
    selected, all data will be written in the standard EMX excel format (
    i.e., packages, entities, attributes). Any additional datasets will be
    added to a new sheet using the <package_entity> name. The workbook can
    then be imported into molgenis. If the user prefers the csv format,
    all components will be writen to csv (e.g., packages.csv, entities.csv,
    attributes.csv, etc.).
    
    @param format (str): write as csv or xlsx (default)
    @param outDir (str): path to save files (default = "." or current dir)
    @param includeData (bool): If True (default), any datasets defined in the yaml
      will be written to file.
    
    """
    if format not in ['csv', 'xlsx']:
      raise ValueError('Error in write: unexpected format ', str(format))
        
    writer = emxWriter(self.packages, self.entities, self.attributes, self.data, self.tags)
    if format == 'xlsx':
      file = outDir + '/' + name + '.' + str(format)
      if path.exists(file):
        remove(file)
      writer.writeXlsx(file, includeData)
    
    if format == 'csv':
      dir = getcwd() if outDir == '.' else path.abspath(outDir)
      if not path.exists(dir):
        raise ValueError('Path ' + dir + 'does not exist')  
      writer.writeCsv(dir, includeData)
 
 
  def write_schema(self, path: str = None):
    """Write Model Schema
    Generate an overview of the model (markdown file).
    
    @param path (str): path to save markdown file
    """
    md = markdownWriter(file = path)
    md.heading(level = 1, title = 'Model Schema')
    md.linebreaks(n = 1)
    md.heading(level = 2, title = "Packages")
    md.linebreaks(n = 1)
    
    # write packages
    pkgs = []
    for pkg in self.packages:
      pkgs.append({
        'Name': pkg.get('name'),
        'Description': pkg.get('description', '-'),
        'Parent': pkg.get('parent', '-')
      })
    md.table(data = pkgs)

    # write entities
    md.linebreaks(n = 1)
    md.heading(level = 2, title = 'Entities')
    md.linebreaks(n = 1)
    entities = []
    for e in self.entities:
      entities.append({
        'Name': e.get('name', '-'),
        'Description': e.get('description', '-'),
        'Package': e.get('package', '-')
      })
    md.table(data = entities)
    
    # write attributes
    md.linebreaks(n = 1)
    md.heading(level = 2, title = 'Attributes')
    for entity in self.entities:
  
      # If attributes do not exist, then don't render schema
      entityPkgName = entity['package'] + '_' + entity['name']
      entityData = list(filter(lambda d: d['entity'] in entityPkgName, self.attributes))
      if entityData:
        md.linebreaks(n = 1)
        md.heading(level = 3, title = f'Entity: {entityPkgName}')
  
        if 'description' in entity:
          md.linebreaks(n = 1)
          md.text(entity['description'])
        else:
          md.linebreaks(n = 1)

        # compile attribute info for table
        entityAttribs = []
        for d in entityData:
          entryAttribs = {
            'Name': d.get('name', '-'),
            'Label': d.get('label', '-'),
            'Description': d.get('description', '-'),
            'Data Type': d.get('dataType', '-')
          }
            
          # add indication if an attribute is a primary key                
          if d.get('idAttribute', None):
            entryAttribs['Name'] = entryAttribs['Name'] + '&#8251;'
          entityAttribs.append(entryAttribs)
          md.table(entityAttribs)
    md.linebreaks(n = 1)
    md.text('Note: The symbol &#8251; denotes attributes that are primary keys')
    md.save()
