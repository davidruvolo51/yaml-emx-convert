#'////////////////////////////////////////////////////////////////////////////
#' FILE: convert.py
#' AUTHOR: d.c.ruvolo
#' CREATED: 2021-09-01
#' MODIFIED: 2021-09-14
#' PURPOSE: convert yaml to emx format
#' STATUS: working; ongoing
#' PACKAGES: see below
#' COMMENTS: see below
#'////////////////////////////////////////////////////////////////////////////

import os
import yaml
from tomark import Tomark
import pandas as pd
from datetime import datetime

# Convert
# @description Convert YAML-EMX markup into EMX- CSV or XLSX file format
#
# @section Instructions
#
# The purpose of the the class `Convert` is to give users the option to write
# Molgenis EMX markup in YAML, and then convert (or compile) into the desired
# file format (csv, excel).
#
# The structure of the yaml file (i.e., property names, syntax, etc.), is very
# similar to the Excel method. There are a few additional features that make
# the process a bit simpler.
#
# You can...
#
# 1.) define default attribute options and apply them globally,
# 2.) define datasets within the YAML (might be useful for smaller entities), and
# 3.) compile file into many formats (csv, xlsx)
#
# At the moment, `Convert` only allows one EMX package per YAML file.
#
# @section The YAML Format
#
# You can write your data model using Molgenis EMX attribute names. Each yaml file
# should be considered a package with one or more entities. The name of the YAML
# file should be the name of the Molgenis package and all entities should be
# written using the <package>_<entity> format. Define the package at the top of
# the file. In addition to the normal EMX package attributes, you can also use
# `version` and `date`. If defined, these attributes will be rendered into
# the description during the conversion (only if indicated to do so).
#
# ```yaml
# name: mypackage
# label: My Package
# description: some description about this package
# version: 0.0.9000
# date: 2021-09-01
# ```
#
# After the package information, used the `defaults` attribute to specify the default
# values for the entities attributes in your model. Use the name `defaults` and list
# all of the EMX attributes and values.
#
# ```yaml
# defaults:
#   dataType: string
#   nillable: true
#   auto: false
#   ...
# ```
#
# Define all entities under the `entities` property. Each entity can be defined using
# `name` property (make sure it is also prefixed with a `-`). Attributes should be
# defined under the respective entity. The property `name` is used to define a new
# 'row' in the attributes sheet. Define all attributes that are needed. The rest
# will be defined using the defaults.
#
# ```yaml
# entities:
#   - name: myEntity
#     label: My Entity
#     description: ...
#     attributes:
#       - name: id
#         label: ID
#         description: Entity identifier
#         idAttribute: true
#         nillable: false
#         ...
#       - name: value
#         dataType: int
#    data:
#       - id: B12345
#         value: 44
#       - id: B54321
#         value: 61
# ```
#
# @section Examples:
#
# Define your data model in yaml file as outlined in the previous section and
# import into your script. Specify the path to the yaml file when creating a
# new instance.
#
# ```python
# import molgenis.convert
#
# c = Convert(files = "path/to/my/file.yml")
# ```
#
# Use the method `convert` to compile the yaml into EMX format. By default,
# if `version` and `date` are defined at the package level, this information
# will be appended to the package description or set as the description (if
# it wasn't provided). Use the argument `includePkgMeta` to disable this
# behavior.
#
# ```python
# c.convert()  # default
# c.convert(includePkgMeta = False)  # to ignore version and date
# ```
#
# Use the method `write` to save the model as xlsx or csv format. There are
# a few options to control this process. These are defined in the list below.
#
# - format: enter 'csv' or 'xlsx'
# - outDir: the output directory (default is '.' or the current directory)
# - includeData: if True (default), all datasets defined in the YAML will be
#       written to file.
#
# ```python
# c.write('xlsx', outDir = 'model/')
# c.write('csv', outDir = 'model/')
# ```
#
# Lastly, you can write the schema to markdown using `write_md`.
#
# ```python
# c.write_schema(path = 'path/to/save/my/model_schema.md')
# ```
#
class Convert:
    def __init__(self, files: list = []):
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
    #
    # @name __yaml__read__
    # @description read yaml file
    # @param file path to file (from self.file)
    # @return dictionary
    #
    def __yaml__read__(self, file):
        with open(file, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as err:
                print("Unable to read yaml:\n" + repr(err))
            stream.close()
    #
    # @name __emx__extract__package__
    # @description extract known EMX package attributes
    # @param data parsed yaml object
    # @param includePkgMeta if TRUE, version and date will be added to description
    # @return ...
    #
    def __emx__extract__package__(self, data, includePkgMeta: bool = True):
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
    #
    # @name __emx__extract__entities
    # @description extract known EMX entity attributes
    # @param data parsed yaml object
    # @param priorityNameKey the priority key name
    # @return list of dictionaries
    #
    def __emx__extract__entities__(self, data, priorityNameKey):
        emx = {'entities': [], 'attributes': [], 'data': {}}
        langAttrs = ('label-', 'description-')
        for entity in data['entities']:
            entityKeys = list(entity.keys())

            # validate required emx properties
            if 'name' not in entityKeys:
                raise ValueError('Error in entity: missing required attribute "name"')
            
            if 'attributes' not in entityKeys:
                raise ValueError('Error in entity: missing required attribute "attributes"')

            # extract entity attributes and append package name automatically
            e = {'package': data['name']}
            for ekey in entityKeys:
                if ekey in self.emxAttributes['entities'] or ekey.startswith(langAttrs):
                    e[ekey] = entity[ekey]
            emx['entities'].append(e)
            
            # append priorityNameKey to approved attributes list
            if priorityNameKey:
                self.emxAttributes['attributes'].append(priorityNameKey)
            
            # check for attributes and extract
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

                # apply default settings if specified
                if data['defaults']:
                    defaultKeys = list(data['defaults'].keys())
                    for dKey in defaultKeys:
                        if dKey not in attrKeys:
                            d[dKey] = data['defaults'][dKey]

                emx['attributes'].append(d)
            
            # check for datasets and extract
            if 'data' in entity:
                name = data['name'] + '_' + entity['name']
                emx['data'][name] = entity['data']

        return emx
    #
    # @name __xlsx__headers
    # @description write unformatted headers to xlsx file
    # @param wb xslxwriter object
    # @param columns list of columns names to write to file
    # @param name sheet name
    #
    def ___xlsx__headers__(self, wb, columns, name):
        sheet = wb.sheets[name]
        format = wb.book.add_format({'bold': False, 'border': False})
        for col, value in enumerate(columns):
            sheet.write(0, col, value, format)
    #
    # @name __write__xlsx__
    # @description write emx to xlsx
    # @param path output path
    #
    def __write__xlsx__(self, path, includeData: bool = True):
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
    #
    # @name __write__csv__
    # @description write emx object to mutiple csv files
    # @param dir output directory (default is the current directory)
    # @param includeData If True (default), all datasets will be written to file
    #
    def __write__csv__(self, dir, includeData: bool = True):

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
    #
    # @name convert
    # @description convert yaml file into EMX structure
    # @param includePkgMeta if TRUE (default), version and date will be added to description
    # @param priorityNameKey For EMX markups that are harmonization projects (i.e.,
    #   multiple `name` attributes), you can set which name attribute gets priority. This
    #   means that you can compile the EMX for different projects. Leave as none if this
    #   doesn't apply to you :-)
    # @return ...
    #
    def convert(self, includePkgMeta: bool = True, priorityNameKey: str = None):
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
    #
    # @name write
    # @description write EMX files
    # @param format write as csv or xlsx (default)
    # @param outDir output directory (defaults to ".")
    # @param includeData If True (default), any datasets defined in the yaml
    #   will be written to file
    # @return None
    def write(
        self,
        name: str = None,
        format: str = 'xlsx',
        outDir: str = '.',
        includeData: bool = True
    ):
        if format not in ['csv', 'xlsx']:
            raise ValueError('Error in write: unexpected format ', str(format))
        
        if format == 'xlsx':
            file = outDir + '/' + name + '.' + str(format)
            if os.path.exists(file):
                os.remove(file)
            self.__write__xlsx__(file, includeData)
        
        if format == 'csv':
            dir = os.getcwd() if outDir == '.' else os.path.abspath(outDir)
            if not os.path.exists(dir):
                raise ValueError('Path ' + dir + 'does not exist')

            self.__write__csv__(dir)
    #
    # @name write_schema
    # @description Write metadata scheme to markdown file
    # @param path path to file
    def write_schema(self, path: str = None):
        with open(path, 'w', encoding = 'utf-8') as md:
            md.write('# Model Schema\n\n')
            
            md.write('## Packages\n\n')
            pkgs = []
            for pkg in self.packages:
                pkgs.append({
                    'Name': pkg.get('name'),
                    'Description': pkg.get('description', '-')
                })
            pkgsTable = Tomark.table(pkgs)
            md.write(pkgsTable)
            
            
            # write entity overview
            md.write('\n## Entities\n\n')
            entities = []
            for e in self.entities:
                entities.append({
                    'Name': e.get('name', '-'),
                    'Description': e.get('description', '-'),
                    'Package': e.get('package', '-')
                })
            entityTable = Tomark.table(entities)
            md.write(entityTable)

            # write data to file
            for entity in self.entities:
                entityPkgName = entity['package'] + '_' + entity['name']
                md.write('\n## Entity: {}\n\n'.format(entityPkgName))
                
                if 'description' in entity:
                    md.write('{}\n\n'.format(entity['description']))
                
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

                attributesTable = Tomark.table(entityAttribs)
                md.write(attributesTable)

            md.close()
