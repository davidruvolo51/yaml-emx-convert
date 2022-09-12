
import pytest
from yamlemxconvert.convert import Convert

emx = Convert(files=['tests/examples/birddata.yaml'])
emx.convert()

def test_emx_properties_are_defined():
  assert bool(emx.packages) & bool(emx.entities) & bool(emx.attributes), 'Primary EMX properties are not defined'

def test_emx_package_is_defined():
  assert len(emx.packages) == 1, 'Model should have one package definition'
  
def test_emx_entities_is_defined():
  assert len(emx.entities) == 6, 'Model should have 6 entities'
  
def test_emx_attributes_is_defined():
  assert len(emx.attributes) == 14, 'Model should have 14 attribute definitions'
  
def test_emx_data_is_defined():
  assert len(emx.data) == 2, 'Model should have 2 datasets'
  
def test_emx_entities_have_valid_package():  
  counter = 0
  for entity in emx.entities:
    if entity['package'] == emx.name:
      counter += 1
  assert counter == len(emx.entities), 'Package is not properly defined in emx.entities'
      
def test_emx_attributes_have_valid_package():
  counter = 0
  entities = [f"{emx.name}_{entity['name']}" for entity in emx.entities]
  for attr in emx.attributes:
    if attr['entity'] in entities:
      counter += 1
  assert counter == len(emx.attributes), 'Package format is not properly defined in emx.attributes'