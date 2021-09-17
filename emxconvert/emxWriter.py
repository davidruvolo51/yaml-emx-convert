"""EMX Excel Writer

Write EMX structure to csv or excel

"""

import pandas as pd

class emxWriter:
    def __init__(self,packages, entities, attributes, data):
        """EMX Writer
        
        Create a new instance of the EMX Writer
        
        Attributes:
            packages (list): EMX packages
            entities (list): EMX entities
            attributes (list): EMX attributes 
            
        Example:
            ```
            writer = emxWriter(packages = pkg, entities = ent, attributes = attribs)
            ```
        
        """
        self.packages = packages
        self.entities = entities
        self.attributes = attributes
        self.data = data

    def ___xlsx__headers__(self, wb, columns, name):
        """Write xlsx headers
        
        Attributes:
            wb: workbook object
            columns: a list of column names
            name: name of the sheet

        """
        sheet = wb.sheets[name]
        format = wb.book.add_format({'bold': False, 'border': False})
        for col, value in enumerate(columns):
            sheet.write(0, col, value, format)
    


    def writeXlsx(self, path, includeData: bool = True):
        """Write XLSX
        
        Write EMX model as XLSX file
        
        Attributes:
            path (string): path to write file
            includeData: if True (default), any data objects defined in the model will be written to file

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
    def writeCsv(self, dir, includeData: bool = True):
        """Write CSV
        
        Write EMX model as csv files
        
        Attributes:
            dir (str): directory to write files into
            includeData (bool): if True (default), any data objects present
                in the EMX will be written to file. 
        """
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