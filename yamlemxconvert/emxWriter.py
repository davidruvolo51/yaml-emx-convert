import pandas as pd
import csv

class emxWriter:
  def __init__(self,packages, entities, attributes, data, tags):
    """EMX Writer
    Create a new instance of the EMX Writer
    
    @param packages (list): EMX packages
    @param entities (list): EMX entities
    @param attributes (list): EMX attributes
    @param tags (list) : EMX tags
        
    @example
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
    @param wb: workbook object
    @param columns: a list of column names
    @param name: name of the sheet

    """
    sheet = wb.sheets[name]
    format = wb.book.add_format({'bold': False, 'border': False})
    for col, value in enumerate(columns):
      sheet.write(0, col, value, format)
    
  def writeXlsx(self, path, includeData: bool = True):
    """Write XLSX
    Write EMX model as XLSX file
    
    @param path (string): path to write file
    @param includeData: If True (default), any data objects defined in the
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
  
  def writeCsv(self, dir, includeData: bool = True):
    """Write CSV
    Write EMX model as csv files

    @param dir (str): directory to write files into
    @param includeData (bool): if True (default), any data objects present
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
      tags.to_csv(dir + '/tags.csv', index = False, quoting=csv.QUOTE_ALL)


class emxWriter2:
  """CSV and XLSX Writer for EMX2"""
  
  def ___xlsx__headers__(self, wb, columns, name):
    """Write xlsx headers
    @param wb workbook object
    @param columns a list of column names
    @param name name of the sheet
    """
    sheet = wb.sheets[name]
    format = wb.book.add_format({'bold': False, 'border': False})
    for col, value in enumerate(columns):
      sheet.write(0, col, value, format)
              
  def writeXlsx(self, model, path):
    """Write EMX as XLSX
    Attributes:
        model (obj) : converted EMX model
        path (str) : output file path
    """
    wb = pd.ExcelWriter(path = path, engine = 'xlsxwriter')
    for entity in model:
      df = pd.DataFrame(model[entity], index=range(0, len(model[entity])))
      df.to_excel(wb, sheet_name = entity, startrow = 1, header = False, index = False)
      self.___xlsx__headers__(wb, df.columns.values, entity)
    wb.save()
      
  def writeCsv(self, model: list = None, dir: str = None):
    """Write EMX2 to CSV
    @param model list of dictionaries
    @param dir output directory
    """
    for entity in model:
      df = pd.DataFrame(model[entity], index = range(0,len(model[entity])))
      df.to_csv(dir + '/' + entity + '.csv', index = False, quoting=csv.QUOTE_ALL)