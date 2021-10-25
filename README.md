# Yaml to EMX Converter

The purpose of **EMX Convert** is to give [Molgenis](https://molgenis.org/) users the option to write Molgenis EMX markup in YAML, and then convert (or compile) into the desired file format (csv, excel).

The structure of the yaml file (i.e., property names, syntax, etc.), is nearly identical to the Excel method. However, there are a few additional features that make the process a more efficient. With the **EMX Convert**, you can to do the following.

- :gear: Default attribute settings: define attribute level defaults and let the converter fill in the rest
- :bar_chart: Data in EMX: define datasets within the YAML (might be useful for smaller entities)
- :card_index_dividers: Multiple output formats: compile EMX models into csv or xlsx format
- :arrows_counterclockwise: Multi-model conversion: render multiple EMX-YAML files into one EMX file
- :scroll: Markdown Schema: generate an overview of your model in a markdown file
- :fire: Build time customization: render the model based on a specific project name (ideal for harmonization projects; i.e., one file multiple models)
- :package: Templates: or shared package-level EMX files across multiple yaml files.
- :label: Tagging: support for semantic tagging

## An introduction to the YAML-EMX format

You can write your data model using standard Molgenis EMX attribute names, but there are a couple of extra features that may be useful for you. This section will provide an introduction on how to define your data model in the YAML-EMX format and an overview on some of the neat features.

### Defining EMX Packages

Each yaml file should be viewed as a single package with one or more entities. To define a package, write the YAML mappings using the standard EMX attributes. For example:

```yaml
name: neuroclinic
label: Neurology Clinic Registry
description: Data about patients and diagnostic imaging performed
version: 1.2.4
date: 2021-09-01
```

Using the YAML-EMX approach, we have introduced the option to record the data model `version` and `date` released. This may be helpful for introducing stricter versioning of your model and working in terms of releases. When you build the data model, these attributes are appended the package description so that it is displayed in the navigator. Using the example above, the description would display in the browser like so:

```text
Data about patients and diagnostic imaging performed (v1.2.4; 2021-09-01)
```

Alternatively, you can define a base EMX package and share it across multiple YAML models. For example, let's say that the main package is `neuroclinic` and in this package, I would like to have several tables and a subpackage. Save the `neuroclinic` markup in a base file (e.g., `base_neuroclinic.yaml`). Create a new file for the entities at the child-level and a file for each subpackage. In the other yaml file, use the mapping `includes` and specify the path to the base file.

```yaml
# in some other emx-yaml file
includes: path/to/base_neuroclinic.yaml
```

### Setting attribute level defaults

Another feature of this package is the option to set attribute level defaults (e.g., `dataType`, `nillable`, etc.). This may be useful for models that have many entities and that have a lot of attributes. This also eliminates the need to set all of the options for each attribute and the hassle of manually changing options if &mdash; or when &mdash; the structure changes. This features allows you to define attribute defaults once and the converter fills in the gaps.

To use this feature, use the mapping `defaults` and use the standard EMX attribute level settings.

```yaml
defaults:
  dataType: string
  nillable: true
  auto: false
```

That's it!

### Defining Entities

Define all entities under the `entities` mapping. Define each entity using the sequence `name` (make sure there's a `-`). All standard EMX names are available, including localization. One of the advantages of the YAML-EMX approach, is that you do not need to write entity names using the `<package>_<entity>` format. This eliminates issues of forgeting to update package names, which fails on import.

```yaml
entities:
  - name: patients
    label: Patients
    label-nl: Patiënten
    description: Information about the patient and when they visited the clinic
    description-nl: Informatie over de patiënten en wanneer ze de kliniek bezochten
```

Repeat this process for all entities.

### Defining Entity Attributes

Attributes can be defined under the appropriate definition using the mapping `attributes`. To make a new definition (i.e., EMX attribute), using the `- name: [attribute name]` format, and then define the options under. Make sure you take advantage of the `defaults` option!

```yaml
entities:
  - name: patients
    label: Patients
    label-nl: Patiënten
    description: Information about the patient
    description-nl: Informatie over de patiënten
    attributes:
      - name: patientID
        idAttribute: true
        dataType: string
        nillable: false
      - name: age
        description: Years of age
        dataType: decimal
      - name: group
        description: group assignment
        dataType: xref
        refEntity: neuroclinic_groups
```

**NOTE!**

It is import to note here that if an attribute is a reference class (e.g., xref, mref, etc.), you must write the `<package>_<entity>` format. This is the only spot where you have to follow this format. It was decided to use this approach as you may want to define lookup tables in another file and build that separately. This allows a bit more flexibility in how you structure your model.

### Defining Entity Data

You can also define datasets within your YAML file. It is not recommended to define raw data. This is designed for building lookup tables.

Let's take the example entity `neuroclinic_groups`. Use the mapping `data` to define datasets and each mapping should correspond to the name defined in the `attributes` block.

```yaml
entities:
  - name: patients
    label: Patients
    label-nl: Patiënten
    description: Information about the patient
    description-nl: Informatie over de patiënten
    attributes:
      - name: patientID
        idAttribute: true
        dataType: string
        nillable: false
      - name: age
        description: Years of age
        dataType: decimal
      - name: group
        description: group assignment
        dataType: xref
        refEntity: neuroclinic_groups
  - name: groups
    label: Groups
    description: Patient groups and descriptions
    attributes:
      - name: id
        idAttribute: true
        dataType: string
        nillable: false
      - name: label
      - name: description
    data:
      - id: groupA
        label: Group A
        description: Group A contains patients that are X
      - id: groupB
        label: Group B
        description: Group B contains patients that are Y
      - id: groupC
        label: Group C
        description: Group C contains patients that are Z
```

## Getting Started

### Usage

Define your data model in yaml file as outlined in the previous section and import into your script. Specify the path to the yaml file when creating a new instance.

```python
from yamlemxconvert.convert import Convert

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
