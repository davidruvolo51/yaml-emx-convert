# Yaml to EMX Converter

Convert YAML-EMX markup into EMX- CSV or XLSX file format

## Introduction

The purpose of the the class `Convert` is to give users the option to write
Molgenis EMX markup in YAML, and then convert (or compile) into the desired
file format (csv, excel).

The structure of the yaml file (i.e., property names, syntax, etc.), is very
similar to the Excel method. There are a few additional features that make
the process a bit simpler.

With the emx converter, you can...

1.) define default attribute options and apply them globally,
2.) define datasets within the YAML (might be useful for smaller entities), and
3.) compile file into many formats (csv, xlsx)
4.) render multiple EMX-YAML files into the same output files
5.) generate a markdown schema
6.) render the model based on a specific project name (ideal for harmonization projects)

### The YAML-EMX Format

You can write your data model using Molgenis EMX attribute names. Each yaml file
should be considered a package with one or more entities. The name of the YAML
file should be the name of the Molgenis package and all entities should be
written using the `<package>_<entity>` format. Define the package at the top of
the file. In addition to the normal EMX package attributes, you can also use
`version` and `date`. If defined, these attributes will be rendered into
the description during the conversion (only if indicated to do so).

```yaml
name: mypackage
label: My Package
description: some description about this package
version: 0.0.9000
date: 2021-09-01
```

After the package information, used the `defaults` attribute to specify the default
values for the entities attributes in your model. Use the name `defaults` and list
all of the EMX attributes and values.

```yaml
defaults:
    dataType: string
    nillable: true
    auto: false
```

Define all entities under the `entities` property. Each entity can be defined using
`name` property (make sure it is also prefixed with a `-`). Attributes should be
defined under the respective entity. The property `name` is used to define a new
'row' in the attributes sheet. Define all attributes that are needed. The rest
will be defined using the defaults.

```yaml
entities:
    - name: myEntity
      label: My Entity
      description: ...
      attributes:
        - name: id
          label: ID
          description: Entity identifier
          idAttribute: true
          nillable: false
        - name: value
          dataType: int
    data:
        - id: B12345
          value: 44
        - id: B54321
          value: 61
```

## Getting Started

### Installation

This package has not been published yet. For now, you can install this library by cloning the repository.

```shell
git clone https://github.com/davidruvolo51/yaml-emx-convert
```

And then building and installing the package locally.

```shell
# build using one of the following commands
tox -e build 
python setup.py sdist
python setup.py bdist_wheel


# install from the compressed file
python3 -m pip install dist/...tar.gz
```

### Usage

Define your data model in yaml file as outlined in the previous section and import into your script. Specify the path to the yaml file when creating a new instance.

```python
from emxconvert.convert import Convert

c = Convert(files = ['path/to/my/file.yml', 'path/to/my/another_file.yml'])
```

Use the method `convert` to compile the yaml into EMX format. By default, if `version` and `date` are defined at the package level, this information will be appended to the package description or set as the description (if it wasn't provided). Use the argument `includePkgMeta` to disable this behavior.

```python
c.convert()  # default
c.convert(includePkgMeta = False)  # to ignore version and date
```

Use the method `write` to save the model as xlsx or csv format. There are a few options to control this process. These are defined in the list below.

- format: enter 'csv' or 'xlsx'
- outDir: the output directory (default is '.' or the current directory)
- includeData: if True (default), all datasets defined in the YAML will be written to file.

```python
c.write('xlsx', outDir = 'model/')
c.write('csv', outDir = 'model/')
```

Lastly, you can write the schema to markdown using `write_md`.

```python
c.write_schema(path = 'path/to/save/my/model_schema.md')
```
