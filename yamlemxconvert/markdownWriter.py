class markdownWriter():
  def __init__(self, file: str = None):
    """Markdown Writer
    Create a new markdown file and write text, write headings, tables,
    specify linebreaks, and more!
    
    @param file (str): location to save file
    """
    self.file = file
    self.md = self.__new__md__(self.file)

  def __new__md__(self, file: str = None):
    """Init Markdown File
    Start a new stream to a markdown file
    
    @param file (str): location to save file
    
    @return stream to md file
    """
    return open(file, mode = 'w', encoding = 'utf-8')

  def __write__(self, *text):
    """Write
    Method to write content to file

    @param *text: content to write
    """
    self.md.write(''.join(map(str, text)))
    
  def save(self):
    """Save and close file
    Close the stream
    """
    self.md.close()

  def linebreaks(self, n: int = 2):
    """Linebreaks
    Insert line break into markdown file
    
    @param n (int): number of line breaks to insert (default: 2)

    Example:
    ```
    md = markdownWriter(file = 'myfile.md')
    md.linebreaks(n = 1)
    ```
    """
    self.__write__('\n' * n)
 
  def heading(self, level: int = 1, title: str = ''):
    """Write Header    
    Create markdown heading 1 through 6.

    @param level (int): markdown heading level, integer between 1 and 6
    @param title (str): content to write
    
    @example
    ```
    md = markdownWriter('myfile.md')
    md.heading(level = 1, title = 'My Document')
    ```
    """
    if not level >= 1 and not level <= 6:
      raise ValueError('Error in write_header: level must be between 1 - 6')
    self.__write__('#' * level,' ',title)
    self.linebreaks(n = 1)

  def text(self, *content):
    """Write Text
    Write paragraph to file

    @param *text: content to write
    """
    self.__write__(*content)
    self.linebreaks(n = 2)

  def table(self, data: list = None):
    """Write a list of dictionaries to file
    
    @param data (list): a list of dictionaries. This method assumes that the
      keys are consistent across all items in the list. 
    """
    char = '-'
    thead = []
    tbody = []
    separators = []
    for i, k in enumerate(data[0].keys()):
      if i == 0:
        thead.append(f'| {k} |')
        separators.append(f'|:{char * len(k) } |')
      else:
        thead.append(f' {k} |')
        separators.append(f':{char * len(k) }|')
            
    for d in data:
      row = []
      for n, el in enumerate(d):
        if n == 0:
          row.append(f'| {d[el]} |')
        else:
          row.append(f' {d[el]} |')
      row.append('\n')
      tbody.append(''.join(row))
    
    self.__write__(''.join(thead),'\n',''.join(separators),'\n',''.join(tbody))

