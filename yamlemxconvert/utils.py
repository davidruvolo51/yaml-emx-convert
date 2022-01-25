import yaml

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