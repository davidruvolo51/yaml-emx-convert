import os
import yaml
import pandas as pd

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


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# READ THE CONTENTS OF A YAML FILE
# Safely Load a .yml file
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def loadYaml(file: str = None):
    """Load YAML File
    
    Read the contents for a YAML file
    
    Attributes:
        file (str): a file path 
    """
    with open(file, 'r') as stream:
        try:
            contents = yaml.safe_load(stream)
        except yaml.YAMLError as err:
            print("Unable to read yaml:\n" + repr(err))
        stream.close()
    return contents



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# MARKDOWN WRITER
# Create a series of methods for writing content to a markdown file. I would
# have used an existing library, but I only need a few methods: write general
# text, write headings, tables, and specifying linebreaks. I really needed
# something to convert datasets to markdown tables.
#
# @example
# To use, create a new instance of the `markdownWriter` class.
# 
# ```python
# from emxconvert.convert import markdownWriter
# md = markdownWriter('myfile.md')
# md.heading(level = 1, 'Hello World')
# md.text('This is my cool markdown file')
# md.save()
# ```
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class markdownWriter():
    def __init__(self, file: str = None):
        """Markdown Writer
        
        Attributes:
            file (str): location to save file
        """
        self.file = file
        self.md = self.__new__md(self.file)
        
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # NEW MD
    # Create a stream to a new md file
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __new__md(self, file: str = None):
        """Init Markdown File
        
        Start a new stream to a markdown file
        
        Attributes:
            file (str): location to create new file
        """
        return open(file, mode = 'w', encoding = 'utf-8')

    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # WRITE
    # Generic writer
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __write__(self, *text):
        """Writer
        
        Method to write content to file
        
        Attributes:
            *text: content to write
        """
        self.md.write(''.join(map(str, text)))
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # SAVE
    # Close stream to markdown file
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def save(self):
        """Save and close file
        """
        self.md.close()


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Write Linebreaks
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Write heading from 1 to 6     
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     
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


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Generic content writer
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def text(self, *content):
        """Write Text
        
        Write paragraph to file
        
        Attributes:
            *text: content to write
        """
        self.__write__(*content)
        self.linebreaks(n = 2)
     
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   # Convert list to markdown table
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def table(self, data: list = None):
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
             


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EMX Writer
# Write EMX structure to CSV of XLSX format.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class emxWriter:
    def __init__(self,packages, entities, attributes, data, tags):
        """EMX Writer
        
        Create a new instance of the EMX Writer
        
        Attributes:
            packages (list): EMX packages
            entities (list): EMX entities
            attributes (list): EMX attributes
            tags (list) : EMX tags
            
        Example:
            ```
            from emxconvert.convert import Convert
            myemx = Convert(...)
            myemx.convert()
            writer = emxWriter(
                packages = myemx.packages,
                entities = myemx.entities,
                attributes = myemx.attributes,
                tags = myemx.tags
            )
            ```
        """
        self.packages = packages
        self.entities = entities
        self.attributes = attributes
        self.data = data
        self.tags = tags

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
    

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Write XLSX
    # Write EMX to excel workbook
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def writeXlsx(self, path, includeData: bool = True):
        """Write XLSX
        
        Write EMX model as XLSX file
        
        Attributes:
            path (string): path to write file
            includeData: If True (default), any data objects defined in the
                model will be written to file.

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
        
        # write tags if defined
        if self.tags:
            tags = pd.DataFrame(self.tags, index = range(0, len(self.tags)))
            tags.to_excel(wb, sheet_name = 'tags', startrow = 1, header = False, index = False)
            self.___xlsx__headers__(wb, tags.columns.values, 'tags')
        
        # write data to file if present and user has indicated so
        if self.data and includeData:
            for dataset in self.data:
                i = range(0, len(self.data[dataset]))
                df = pd.DataFrame(self.data[dataset], index = i)
                df.to_excel(wb, sheet_name = dataset, startrow = 1, header = False, index = False)
                self.___xlsx__headers__(wb, df.columns.values, dataset)

        wb.save()
    

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # WRITE CSV
    # Write emx to csv format
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
        
        # write data to file if present and user has indicated so
        if self.data and includeData:
            for dataset in self.data:
                i = range(0, len(self.data[dataset]))
                df = pd.DataFrame(self.data[dataset], index = i)
                df.to_csv(dir + '/' + dataset + '.csv', index = False)

        # write tags if defined
        if self.tags:
            tags = pd.DataFrame(self.tags, index = range(0, len(self.tags)))
            tags.to_csv(dir + '/tags.csv', index = False)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Convert
# Read and transform a YAML-EMX markup into excel (CSV, xlsx) EMX format
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
        self.__init__fields__()
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # INIT AND RESET OBJECTS
    # Set all internal objects to their default state
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__fields__(self):
        self.packages = []
        self.entities = []
        self.attributes = []
        self.tags = []
        self.data = {}
        self.priorityNameKey = None
        self.lang_attrs = ('label-', 'description-')
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # EXTRACT EMX PROPERTIES
    # Pull all known package attributes. If `includePkgMeta`, date and version
    # will be extracted (if available) and appended to the package description
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __emx__extract__package__(self, data, includePkgMeta: bool = True):
        """Extract EMX Package Metadata
        
        Extract known EMX package attributes
        
        Attributes:
            data (list): contents of a yaml file
            includePkgMeta (bool): if TRUE (default), version and date will
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
            if 'date' in keys:
                pkgMeta['date'] = str(data['date'])
            if pkgMeta:
                if 'description' in keys:
                    pkg['description'] = '{} ({})'.format(
                        pkg['description'],
                        ', '.join(pkgMeta.values())
                    )
                else:
                    pkg['description'] = '; '.join(pkgMeta.values())
        return pkg


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # EXTRACT EMX TAGS
    # Tags are defined using the 'tagDefinitions' property. This property name
    # was selected to avoid name conflicts when 'tags' is used by properties
    # defined at the same level in the YAML. This method pulls valid keys.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __emx__extract__tags__(self, tags):
        """Extract known EMX tags
        
        @param tags (list) : if present, a list of dictionaries containing
            tag definitions. Properties must be defined under the
            `tagDefinitions` tag.
        """
        for tag in tags:
            keys = list(tag.keys())
            for k in keys:
                if not (k in __emx__keys__tags__):
                    del tag[k]
        return tags
                    


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # EXTRACT EMX PROPERTIES
    # For each entity, pull entity information and build attributes.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __emx__extract__entities__(self, data):
        """Extract known EMX entity attributes
        
        Attributes:
            data (list): contents of a yaml file
        """
        emx = {'entities': [], 'attributes': [], 'data': {}}
        for entity in data['entities']:

            entityKeys = list(entity.keys())

            if 'name' not in entityKeys:
                raise ValueError(
                    'Error in entity: missing required attribute "name"'
                )
            
            if 'attributes' not in entityKeys:
                raise ValueError(
                    'Error in entity: missing required attribute "attributes"'
                )

            # pull entity info
            e = {'package': data['name']}
            for ekey in entityKeys:
                if ekey in __emx__keys__enty__ or ekey.startswith(self.lang_attrs):
                    e[ekey] = entity[ekey]
            emx['entities'].append(e)
            

            # pull attribute definitions
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
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # CONVERT
    # `convert` is the primary method for generating EMX models. This method
    # reads one or more YAML files and transforms them into the main EMX
    # components: packages, entities, attributes, and data. The component data
    # is specific to this project. The purpose of `data` is store any datasets
    # that are defined in the yaml file. This is useful if the user would like
    # to define a reference entity in the model.
    #
    # There are couple of unique features that are available.
    #
    # 1. **Data**: users can define datasets directly in the yaml
    # 2. **Validation**: `convert` provides some validation such as checking
    #       for incorrect EMX attribute names, invalid dataTypes, etc. This
    #       may help eliminate import errors.
    # 3. **Multiple Models**: In some situations, you may need to have a
    #       single model that has multiple names per attributes. At the time of
    #       conversion, you can specify the model you wish to generate.
    # 4. **Multiple files**: render and write multiple models to file
    # 5. **Include base package**: If you have multiple subpackages within a
    #       model, you can use the attribute `include` to read and compile 
    #       the parent package EMX.
    # 6. **Metadata**: You can define and include EMX metadata at the package
    #       level. Support is available for `date` and `version`.
    # 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def convert(self, includePkgMeta: bool = True, priorityNameKey: str = None):
        """Convert Model
        
        Convert yaml file into EMX structure
        
        Attributes:
            includePkgMeta (bool): if TRUE (default), version and date will
                be added to description
            priorityNameKey (str): For EMX markups that are harmonization
                projects (i.e., multiple `name` attributes), you can set
                which name attribute gets priority. This means that you can
                compile the EMX for different projects. Otherwise, leave this
                as none if this doesn't apply to you :-)

        """
        # make sure internal slots are reset
        self.__init__fields__()
        
        # if specified, set `priorityNameKey`
        if priorityNameKey:
            self.priorityNameKey = priorityNameKey
        
        # process all named files 
        for file in self.files:
            print('Processing: {}'.format(file))
            yaml = loadYaml(file)
        
            keys = list(yaml.keys())
            if ('name' not in keys) and ('include' not in keys):
                raise ValueError('Error in convert: missing required attribute "name"')
            

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
                emx = {
                    **self.__emx__extract__entities__(yaml)
                }

            # append EMX components to model where applicable
            if 'entities' in emx: self.entities.extend(emx['entities'])
            if 'attributes' in emx: self.attributes.extend(emx['attributes'])
            if 'data' in emx: self.data.update(emx['data'])
    
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # WRITE
    # Write the EMX model to file as csv or xlsx. If excel workbook format is
    # selected, all data will be written in the standard EMX excel format (
    # i.e., packages, entities, attributes). Any additional datasets will be
    # added to a new sheet using the <package_entity> name. The workbook can
    # then be imported into molgenis. If the user prefers the csv format,
    # all components will be writen to csv (e.g., packages.csv, entities.csv,
    # attributes.csv, etc.). 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
            
        writer = emxWriter(self.packages, self.entities, self.attributes, self.data, self.tags)
        
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
    

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # WRITE SCHEMA
    # Using the converted YAML-EMX objects, write the model to markdown file.
    # The file should be provide an overview of the packages defined, entities
    # for each package and all attributes. Only a select set of columns are
    # rendered for the tables.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
