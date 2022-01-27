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
- :label: Tagging: support for semantic tags
- :partying_face: EMX2 Support!!!

## An introduction to the YAML-EMX format

### What is EMX?

So what is the EMX format? Before we dive into the contents of this repo, I would like to start with a gentle introduction to EMX. EMX is the underlying data structure for [Molgenis databases](https://www.molgenis.org/), which is an open source database platform that allows researchers and bioinformaticians to accelerate scientific collaborations. EMX is the underlying data modeling format for creating a Molgenis database. EMX models are flexible and user-friendly as they can be created in xlsx and csv formats.

_**Why did you build an EMX converter?**_

We wanted to make the process of writing EMX models even more flexible. One of the many exciting features in EMX2 (the next generatation of Molgenis) is support for YAML-EMX models. However, this isn't available for EMX1. This python library was created to give Molgenis users the option to write EMX1 models in a YAML file, and then build them into the Excel or CSV formats.

### Writing EMX in YAML format

You can write your data model using standard Molgenis EMX attribute names, but there are a couple of extra features that may be useful for you. This section will provide an introduction on how to define your data model in the YAML-EMX format and an overview on some of the neat features.

#### Defining EMX Packages

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

#### Setting attribute level defaults

Another feature of this package is the option to set attribute level defaults (e.g., `dataType`, `nillable`, etc.). This may be useful for models that have many entities and that have a lot of attributes. This also eliminates the need to set all of the options for each attribute and the hassle of manually changing options if &mdash; or when &mdash; the structure changes. This features allows you to define attribute defaults once and the converter fills in the gaps.

To use this feature, use the mapping `defaults` and use the standard EMX attribute level settings.

```yaml
defaults:
  dataType: string
  nillable: true
  auto: false
```

That's it!

#### Defining Entities

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

#### Defining Entity Attributes

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

> It is import to note here that if an attribute is a reference class (e.g., xref, mref, etc.), you must write the `<package>_<entity>` format. This is the only spot where you have to follow this format. It was decided to use this approach as you may want to define lookup tables in another file and build that separately. This allows a bit more flexibility in how you structure your model.

#### Defining Entity Data

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

To get started, the following items are required.

- A Molgenis instance: Checkout the [Try Out Molgenis Guide](https://molgenis.gitbook.io/molgenis/readme/guide-try-out-molgenis) for more information.
- Install the yaml to emx converter: `pip install yamlemxconvert`
- A blank yaml file
- A blank python script

Define your data model in yaml file as outlined in the previous section.

In the python file, import the `Convert` class and specify the files that you would like to build.

```python
from yamlemxconvert.convert import Convert
emx = Convert(files = ['path/to/my/model.yaml'])
```

All files will be rendered into the same Molgenis package (i.e., database). If you would like to have a subpackage, create a second YAML file and specify it in the `files` argument. This approach is useful if your database has many lookup tables. Rather than overcrowding the main table list (i.e., the list of tables that the users will interact with), it's best to store these in a subpackage.

```python
emx = Convert(files = ['path/to/my/model.yaml', 'path/to/my/model_lookups.yaml'])
```

Next, convert your model.

```python
emx.convert()  # default
```

The `convert` method will perform some *light* validation of your model. It will look for invalid data types and throw errors is required attributes are missing.

### Convert options: Model metadata

By default, if `version` and `date` are defined at the package level, this information will be appended to the package description or set as the description (if it wasn't provided to begin with). Use the argument `includePkgMeta` to disable this behavior.

```python
emx.convert(includePkgMeta = False)  # to ignore version and date
```

### Convert options: defining multiple EMX models in one YAML file

Another cool feature of the `yamlemxconvert` package, is the ability to define a single model that can be *built* for multiple projects. This is useful for harmonization projects or if you would like to have a single model that can be use in more than one project that have different name preferences (ideally these projects should be using a harmonized model, but that's a different story). This can be done by appending the project name to the EMX attribute `name`.

To demonstrate this, let's take the neurology clinic registry example used that was used in the previous section.

```yaml
name: neuroclinic
label: Neurology Clinic Registry
description: Data about patients and diagnostic imaging performed
version: 1.2.4
date: 2021-09-01

entities:
  - name: patients
    label: Patients
    description: Information about the patient
    attributes:
      - name: patientID
        idAttribute: true
        dataType: string
        nillable: false
      - name: age
        name-projectA: currentAge
        name-projectB: ageOfPatient
        description: Years of age
        dataType: decimal
      - name: group
        name-projectA: groupAllocation
        name-projectB: groupAssignment
        description: group assignment
        dataType: xref
        refEntity: neuroclinic_groups
```

In this example, we've created an additional `name` attributes for age and group and specified the preferred name for each project. At build time, we can specify which project we are building the model for (`projectA` or `projectB`) via the `priorityNameKey` argument.

```python
emx.convert(priorityNameKey = 'name-projectA')
```

The built model consists of the attributes specific to projectA.

### Saving your model

Once the model has been built, use the method `write` to save the model as an xlsx or csv file. There are a few options to control this process.

- `format`: enter 'csv' or 'xlsx'
- `outDir`: the output directory (default is '.' or the current directory)
- `includeData`: if True (default), all datasets defined in the YAML will be written to file.

```python
emx.write(format = 'xlsx', outDir = 'public/')
emx.write(format = 'csv', outDir = 'public/')
emx.write(format = 'xlsx', outDir = 'public/', includeData = False)
```

In addition, you can generate a markdown schema of your model. The schema provides an overview of your model that can be shared with collaborators. The method `write_schema` takes one argument `path`, which is used to specify the output location of the markdown file.

```python
emx.write_schema(path = 'public/model_schema.md')
```

### Converting to EMX2

The `yamlemxconvert` package includes basic support for converting your YAML-EMX model into EMX2. The process is, for the most part, identical to the YAML-EMX method. To get started, import the `Convert2` class.

```python
from yamlemxconvert.convert import Convert2
```

Create a new instance and enter the path to the YAML file. The major change from the EMX1 `Convert` method is that only one model can be rendered at a time. (This is most likely a temporary limitation.)

```python
emx2 = Convert2(file='path/to/my/model.yaml')
```

Convert the model using the `convert` method.  Like the EMX1 convert method you can choose to ignore any datasets defined in the YAML file using the argument `ignoreData` (default: `False`).

A new feature is the ability to decide if you would like to flatten nested EMX packages. In EMX1, you may have a package within a package, but nested schemas aren't allowed in EMX2. You can either flatten the schemas or separate create a new schema as a shared resource. By default, this option is set to `True`.

```python
emx2.convert()
```

Lastly, write the model. At this time, `write` supports to `xslx` format. Support for other formats is in progress.

```python
emx2.write(name = 'mymodel', outDir = 'path/to/dir/')
```

## Contributing

Any suggestions and feedback are welcome! Feel free to create a new issue.

If you would like to contribute to the code base, you will need to python >=3.6 installed and the following python libraries: `PyYaml` and `pandas`. When you have finished implementing new features or fixes, test it with a model. You can use one of the example models provided in `dev/example/` or you can create a new one.

### Developing

If you would like to work on this package and submit your changes, use the following build steps.

#### 1. Set version number

This project uses [bumpversion](https://pypi.org/project/bumpversion/) to increment the version across multiple files. Use one of the following yarn scripts to update the version.

```shell
yarn bumpversion:patch
yarn bumpversion:minor
yarn bumpversion:major
```

#### 2. Build and check

Before deployment, build the package and check it.

```shell
yarn py:build
yarn py:check
```

You may also want to install `yamlemxconvert` locally before deployment and test it locally to make sure everything works.

```shell
yarn py:install
```

### 3. Deploy

Deploy `yamlemxconvert` to [Test.PyPi](https://test.pypi.org/) and make sure everything runs as expected.

```shell
yarn deploy:test
```

Fix any errors and then deploy to [PyPi](https://pypi.org/).

```shell
yarn deploy:prod
```
