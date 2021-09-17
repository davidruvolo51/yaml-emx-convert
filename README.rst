==========
Emx Convert
==========


Convert YAML-EMX markup into EMX- CSV or XLSX file format


Description
===========

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



.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.0.2. For details and usage
information on PyScaffold see https://pyscaffold.org/.
