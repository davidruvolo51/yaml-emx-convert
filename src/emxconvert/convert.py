
import os
import yaml
from datetime import datetime
import pandas as pd


# EMX Attributes
# define known EMX attributes
__emx__keys__pkgs__ = ['name', 'label', 'description', 'parent', 'tags']
__emx__keys__enty__ = ['name','label','extends','package','abstract','description', 'backend', 'tags']
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
    'expression'
]

__emx__keys__dtype__ = [
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


# LoadYaml
# Load contents of a yaml file
def loadYaml(file: str = None):
    """Load YAML File
    
    Read the contents for a YAML file
    
    Attributes:
        file (str): a file path 
    """
    with open(file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as err:
            print("Unable to read yaml:\n" + repr(err))
        stream.close()



# Markdown Writer
# Create a new markdown file and write content into it
class markdownWriter():
    
    def __init__(self, file: str = None):
        """Markdown Writer
        
        Attributes:
            file (str): location to save file
        """
        self.file = file
        self.md = self.__init__md__(self.file)
        
        
    def __init__md__(self, file: str = None):
        """Init Markdown File
        
        Start a new stream to a markdown file
        
        Attributes:
            file (str): location to create new file
        """
        return open(file, mode = 'w', encoding = 'utf-8')

        
    def __write__(self, *text):
        """Writer
        
        Method to write content to file
        
        Attributes:
            *text: content to write
        """
        self.md.write(''.join(map(str, text)))
    

    def save(self):
        """Save and close file
        """
        self.md.close()


    def linebreaks(self, n: int = 2):
        """Linebreaks
        
        Insert line break into markdown file
        
        Attributes:
            n (int): number of line breaks to insert (default: 2)

        Example:
            ```
            md = markdownWriter(file = 'path/to/file.md')
            md.linebreaks(n = 1)
            ```
        """
        self.__write__('\n' * n)

     
    def heading(self, level: int = 1, title: str = ''):
        """Write Header
        
        Create markdown heading 1 through 6.
        
        Attributes:
            level (int): markdown heading level, integer between 1 and 6
            title (str): content to write
        
        Example:
            ```
            md = markdownWriter('path/to/file.md')
            md.heading(level = 1, title = 'My Document')
            ```
        """
        if not level >= 1 and not level <= 6:
            raise ValueError('Error in write_header: level must be between 1 - 6')

        self.__write__('#' * level,' ',title)
        self.linebreaks(n = 1)


    def text(self, *content):
        """Write Text
        
        Write paragraph to file
        
        Attributes:
            *text: content to write
        """
        self.__write__(*content)
        self.linebreaks(n = 2)
     
   
    def table(self, data):
        """
        Write a list of dictionaries to file
        
        Attributes:
            data (list): a list of dictionaries. This method assumes that the
                keys are consistent across all items in the list. 
        """
        char = '-'
        thead = []
        tbody = []
        separators = []
        for i, k in enumerate(data[0].keys()):
            if i == 0:
                thead.append(f'| {k} |')
                separators.append(f'|:{char * len(k) } |')
            else:
                thead.append(f' {k} |')
                separators.append(f':{char * len(k) }|')
                
        for d in data:
            row = []
            for n, el in enumerate(d):
                if n == 0:
                    row.append(f'| {d[el]} |')
                else:
                    row.append(f' {d[el]} |')
            row.append('\n')
            tbody.append(''.join(row))
        
        self.__write__(''.join(thead),'\n',''.join(separators),'\n',''.join(tbody))
             


# EMX Writer
# Write EMX structure to CSV of XLSX format
class emxWriter:
    def __init__(self,packages, entities, attributes, data):
        """EMX Writer
        
        Create a new instance of the EMX Writer
        
        Attributes:
            packages (list): EMX packages
            entities (list): EMX entities
            attributes (list): EMX attributes 
            
        Example:
            ```
            writer = emxWriter(packages = pkg, entities = ent, attributes = attribs)
            ```
        
        """
        self.packages = packages
        self.entities = entities
        self.attributes = attributes
        self.data = data

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
    


    def writeXlsx(self, path, includeData: bool = True):
        """Write XLSX
        
        Write EMX model as XLSX file
        
        Attributes:
            path (string): path to write file
            includeData: if True (default), any data objects defined in the model will be written to file

        """
        wb = pd.ExcelWriter(path, engine = 'xlsxwriter')

        pkgs = pd.DataFrame(self.packages, index=range(0, len(self.packages)))
        enty = pd.DataFrame(self.entities, index = range(0, len(self.entities)))
        attr = pd.DataFrame(self.attributes, index = range(0, len(self.attributes)))
        
        pkgs.to_excel(wb, sheet_name = 'packages', startrow = 1, header = False, index = False)
        enty.to_excel(wb, sheet_name = 'entities', startrow = 1, header = False, index = False)
        attr.to_excel(wb, sheet_name = 'attributes', startrow = 1, header = False, index = False)
        
        self.___xlsx__headers__(wb, pkgs.columns.values, 'packages')
        self.___xlsx__headers__(wb, enty.columns.values, 'entities')
        self.___xlsx__headers__(wb, attr.columns.values, 'attributes')
        
        if self.data and includeData:
            for dataset in self.data:
                i = range(0, len(self.data[dataset]))
                df = pd.DataFrame(self.data[dataset], index = i)
                df.to_excel(wb, sheet_name = dataset, startrow = 1, header = False, index = False)
                self.___xlsx__headers__(wb, df.columns.values, dataset)

        wb.save()
    

    def writeCsv(self, dir, includeData: bool = True):
        """Write CSV
        
        Write EMX model as csv files
        
        Attributes:
            dir (str): directory to write files into
            includeData (bool): if True (default), any data objects present
                in the EMX will be written to file. 
        """
        pkgs = pd.DataFrame(self.packages, index=[0])
        enty = pd.DataFrame(self.entities, index = range(0, len(self.entities)))
        attr = pd.DataFrame(self.attributes, index = range(0, len(self.attributes)))

        pkgs.to_csv(dir + '/packages.csv', index = False)
        enty.to_csv(dir + '/entities.csv', index = False)
        attr.to_csv(dir + '/attributes.csv', index = False)
        
        if self.data and includeData:
            for dataset in self.data:
                i = range(0, len(self.data[dataset]))
                df = pd.DataFrame(self.data[dataset], index = i)
                df.to_csv(dir + '/' + dataset + '.csv', index = False)




# Convert
# Primary class for reading, transforming, and writing EMX-YAML markup
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
            if k in __emx__keys__pkgs__ or k.startswith(('label-', 'description-')):
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
                if ekey in __emx__keys__enty__ or ekey.startswith(langAttrs):
                    e[ekey] = entity[ekey]
            emx['entities'].append(e)
            

            __valid__emx__attr__ = __emx__keys__attr__
            if priorityNameKey:
                __valid__emx__attr__.append(priorityNameKey)
            

            attributes = entity['attributes']
            for attr in attributes:
                attrKeys = list(attr.keys())
                d = {'entity': data['name'] + '_' + entity['name']}
                for aKey in attrKeys:
                    if aKey in __valid__emx__attr__ or aKey.startswith(langAttrs):
                        d[aKey] = attr[aKey]
                        
                # adjust priorityKey if mulitple `name` attributes are used
                if priorityNameKey and priorityNameKey in d:
                    if d[priorityNameKey] != 'none':
                        d.pop('name')
                        d['name'] = d.get(priorityNameKey, None)
                        d.pop(priorityNameKey, None)

                # provide dataType validation
                if 'dataType' in d:
                    if d['dataType'] not in __emx__keys__dtype__:
                        raise ValueError(
                            'Error in Convert:\n In entity {}, attribute {} has invalid dataType {}.'
                            .format(d['entity'], d['name'], d['dataType'])
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
            self.yaml = loadYaml(file)
        
            keys = list(self.yaml.keys())
            if 'name' not in keys:
                raise ValueError('Error in convert: missing required attribute "name"')
            
            emx = {}            
            if 'entities' in keys:
                emx = {
                    **self.__emx__extract__entities__(self.yaml, priorityNameKey)
                }

            emx['packages'] = self.__emx__extract__package__(self.yaml, includePkgMeta)

            self.packages.extend([emx['packages']])
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
