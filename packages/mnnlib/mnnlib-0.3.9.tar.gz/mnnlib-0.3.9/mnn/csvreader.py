import csv

from mnn.csvdata import csvdata

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

class csvreader:
  """
  simple class to read csv files
  returns a csvdata class
  """
  def __init__(self,file_name:str, delm=","):
    self.file_name = file_name
    self.delm = delm


  def read(self):
    """
    starts the reading of csv data
    """
    data = csvdata()
    indexes = []
    with open(self.file_name, 'r', encoding='utf8') as csvfile:
      reader = csv.reader(csvfile,delimiter=self.delm)
      line_num = 0
      for row in reader:
        if line_num == 0:
          for name in row:
            indexes.append(name)
            data.add_index(name)
        else:
          for i,n in zip(indexes,row):
            n = float(n) if n.isnumeric() or isfloat(n) else n
            n = n if n != "" else 1.0
            data.add_data(i,n)
        line_num += 1
    return data