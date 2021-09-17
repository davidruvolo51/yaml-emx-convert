
import os
import yaml
from datetime import datetime
from emxconvert.markdownWriter import markdownWriter
from emxconvert.emxWriter import emxWriter


class Convert:
    def __init__(self, files: list = []):
        """Convert
        
        Create a new instance of the YAML to EMX converter.
        
        Attributes:
            files (list): a list of files to convert
        
        Examples:
        
            ```
            c = Convert(files = ['path/to/my_model.yml', 'path/to/my_model_1.yml'])
            ```
        """
        self.files = files
        self.packages = []
        self.entities = []
        self.attributes = []
        self.data = {}
        self.yaml = False
        self.emxAttributes = {
            'packages': ['name', 'label', 'description', 'parent', 'tags'],
            'entities': ['name','label','extends','package','abstract','description', 'backend', 'tags'],
            'attributes': [
                'entity','name','dataType',
                'refEntity','nillable','idAttribute','auto','description',
                'rangeMin','rangeMax','lookupAttribute','label','aggregateable',
                'labelAttribute','readOnly','tags','validationExpression',
                'visible','defaultValue', 'partOfAttribute', 'expression'
            ]
        }


    def __yaml__read__(self, file):
        """Read YAML File
        Attributes:
            file (str): a file path 
        """
        with open(file, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as err:
                print("Unable to read yaml:\n" + repr(err))
            stream.close()
    
    

    def __emx__extract__package__(self, data, includePkgMeta: bool = True):
        """Extract EMX Package Metadata
        
        Extract known EMX package attributes
        
        Attributes:
            data (list): contents of a yaml file
            includePkgMeta (bool): if TRUE (default), version and date will be added to description

        """
        pkg = {}
        keys = list(data.keys())
        for k in keys:
            if k in self.emxAttributes['packages'] or k.startswith(('label-', 'description-')):
                pkg[k] = data[k]
        
        if includePkgMeta:
            pkgMeta = {}
            if 'version' in keys:
                pkgMeta['version'] = "v" + str(data['version'])
            if 'date' in keys:
                pkgMeta['date'] = str(datetime.strptime(str(data['date']), "%Y-%m-%d").date())
            if pkgMeta:
                if 'description' in keys:
                    pkg['description'] = pkg['description'] + ' (' + ', '.join(pkgMeta.values()) + ')'
                else:
                    pkg['description'] = ', '.join(pkgMeta.values())
        return pkg



    def __emx__extract__entities__(self, data, priorityNameKey):
        """Extract known EMX entity attributes
        
        Attributes:
            data (list): contents of a yaml file
            priorityNameKey (string): If supplied, the model will be rendered according
                to the priority name key (useful if model contains multiple name attributes)

        """
        emx = {'entities': [], 'attributes': [], 'data': {}}
        langAttrs = ('label-', 'description-')
        for entity in data['entities']:

            entityKeys = list(entity.keys())

            if 'name' not in entityKeys:
                raise ValueError('Error in entity: missing required attribute "name"')
            
            if 'attributes' not in entityKeys:
                raise ValueError('Error in entity: missing required attribute "attributes"')

            e = {'package': data['name']}
            for ekey in entityKeys:
                if ekey in self.emxAttributes['entities'] or ekey.startswith(langAttrs):
                    e[ekey] = entity[ekey]
            emx['entities'].append(e)
            

            if priorityNameKey:
                self.emxAttributes['attributes'].append(priorityNameKey)
            

            attributes = entity['attributes']
            for attr in attributes:
                attrKeys = list(attr.keys())
                d = {'entity': data['name'] + '_' + entity['name']}
                for aKey in attrKeys:
                    if aKey in self.emxAttributes['attributes'] or aKey.startswith(langAttrs):
                        d[aKey] = attr[aKey]
                
                if priorityNameKey and priorityNameKey in d:
                    if d[priorityNameKey] != 'none':
                        d.pop('name')
                        d['name'] = d.get(priorityNameKey, None)
                        d.pop(priorityNameKey, None)


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
        
        Convert yaml file into EMX structure
        
        Attributes:
            includePkgMeta (bool): if TRUE (default), version and date will be added to description
            priorityNameKey (str): For EMX markups that are harmonization projects (i.e.,
                multiple `name` attributes), you can set which name attribute gets priority. This
                means that you can compile the EMX for different projects. Leave as none if this
                doesn't apply to you :-)

        """
        for file in self.files:
            print('Processing: {}'.format(file))
            self.yaml = self.__yaml__read__(file)
        
            keys = list(self.yaml.keys())
            if 'name' not in keys:
                raise ValueError('Error in convert: missing required attribute "name"')
        
            if 'entities' not in keys:
                raise ValueError('Error in convert: missing "entities"')
            
            emx = {
                'packages': self.__emx__extract__package__(self.yaml, includePkgMeta),
                **self.__emx__extract__entities__(self.yaml, priorityNameKey)
            }

            self.packages.extend([emx['packages']])
            self.entities.extend(emx['entities'])
            self.attributes.extend(emx['attributes'])
            self.data.update(emx['data'])
    
    
    
    def write(
        self,
        name: str = None,
        format: str = 'xlsx',
        outDir: str = '.',
        includeData: bool = True
    ):
        """Write EMX to csv or xlsx
        
        Attributes:
            format (str): write as csv or xlsx (default)
            outDir (str): path to save files (default = "." or current dir)
            includeData (bool): If True (default), any datasets defined in the yaml
                will be written to file
        
        """
        if format not in ['csv', 'xlsx']:
            raise ValueError('Error in write: unexpected format ', str(format))
            
        writer = emxWriter(self.packages, self.entities, self.attributes, self.data)
        
        if format == 'xlsx':
            file = outDir + '/' + name + '.' + str(format)
            if os.path.exists(file):
                os.remove(file)
            writer.writeXlsx(file, includeData)
        
        if format == 'csv':
            dir = os.getcwd() if outDir == '.' else os.path.abspath(outDir)
            if not os.path.exists(dir):
                raise ValueError('Path ' + dir + 'does not exist')
            
            writer.writeCsv(dir, includeData)
    

    def write_schema(self, path: str = None):
        """Write Model Schema
        
        Generate an overview of the model (markdown file).
        
        Attributes:
            path (str): path to save markdown file

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
                'Description': pkg.get('description', '-')
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
            entityPkgName = entity['package'] + '_' + entity['name']
            md.linebreaks(n = 1)
            md.heading(level = 3, title = f'Entity: {entityPkgName}')
        
            if 'description' in entity:
                md.linebreaks(n = 1)
                md.text(entity['description'])

            entityData = list(filter(lambda d: d['entity'] in entityPkgName, self.attributes))
            entityAttribs = []

            for d in entityData:
                entityAttribs.append({
                    'Name': d.get('name', '-'),
                    'Label': d.get('label', '-'),
                    'Description': d.get('description', '-'),
                    'Data Type': d.get('dataType', '-'),
                    'ID Attribute': d.get('idAttribute', '-')
                })
            md.table(entityAttribs)
        md.save()
