
EMX Convert
============

The purpose of **EMX Convert** is to give [Molgenis](https://molgenis.org/) users the option to write Molgenis EMX markup in YAML, and then convert (or compile) into the desired file format (csv, excel).

The structure of the yaml file (i.e., property names, syntax, etc.), is nearly identical to the Excel method. However, there are a few additional features that make the process a bit simpler. With the emx converter, you can...

1.) define and apply default options
2.) define datasets within the YAML (might be useful for smaller entities)
3.) compile EMX models into csv or xlsx format
4.) render multiple EMX-YAML files into one EMX file
5.) generate a markdown schema
6.) render the model based on a specific project name (ideal for harmonization projects)


Getting Started
=================

The YAML-EMX Format
---------------------

You can write your data model using Molgenis EMX attribute names. Each yaml file should be considered a package with one or more entities. The name of the YAML file should be the name of the Molgenis package and all entities should be written using the `<package>_<entity>` format. Define the package at the top of the file. In addition to the normal EMX package attributes, you can also use `version` and `date`. If defined, these attributes will be rendered into the description during the conversion (only if indicated to do so).

.. code-block:: default
    name: mypackage
    label: My Package
    description: some description about this package
    version: 0.0.9000
    date: 2021-09-01

After the package information, used the `defaults` attribute to specify the default values for the entities attributes in your model. Use the name `defaults` and list all of the EMX attributes and values.

.. code-block:: default
    defaults:
        dataType: string
        nillable: true
        auto: false

Define all entities under the `entities` property. Each entity can be defined using `name` property (make sure it is also prefixed with a `-`). Attributes should be defined under the respective entity. The property `name` is used to define a new 'row' in the attributes sheet. Define all attributes that are needed. The rest will be defined using the defaults.

.. code-block:: default
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



.. _license:

=======
License
=======

.. include:: ../LICENSE.txt
