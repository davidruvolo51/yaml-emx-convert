
import pytest
from yamlemxconvert.convert2 import Convert2

emx2 = Convert2(file = 'tests/examples/birddata.yaml')
emx2.convert()


def test_model_properties_exist():
  assert bool(emx2.model) & bool(emx2.name) & bool(emx2.filename)
  
def test_model_structure_objects():
  assert list(emx2.model.keys()) == ['molgenis','states','species'], 'EMX2 model is not properly structured.'