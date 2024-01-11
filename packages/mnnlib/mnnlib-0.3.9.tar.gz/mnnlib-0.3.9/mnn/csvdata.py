from mnn.dataset import dataset


class csvdata:
  """
  data class for csv files
  created by csvreader class
  can output to dataset class
  """
  def __init__(self):
    self.indexes = []
    self.data = []
    self.tocombin = []
    self.tocombout = []

  def add_index(self, index):
    """
    add index to data
    """
    self.indexes.append(index)
    self.data.append([])

  def __str__(self):
    t = 'indexes: '
    t += ' '.join(self.indexes)
    return t
  
  def add_data(self, index,data):
    """
    adds data to the csvdata class
    """
    if index not in self.indexes:
      raise Exception(f"Index '{index}' not in data")
    self.data[self.indexes.index(index)].append(data)

  def add_input(self,index):
    """
    this adds indexes to the input for the generated dataset
    """
    self.tocombin.append(index)
    
  def add_output(self,index):
    """
    this adds indexes to the output for the generated dataset
    """
    self.tocombout.append(index)

  def gen_data(self) -> dataset:

    """
    creates dataset based on data in class
    """

    #this is a fucking mess
    #i am going to kill myself
    #:(
    
    d = dataset()
    ins = [self.data[self.indexes.index(r)] for r in self.tocombin]
    outs = [self.data[self.indexes.index(r)] for r in self.tocombout]
    in2 = [[] for _ in range(len(ins[0]))]
    out = [[] for _ in range(len(outs[0]))]
    for i in ins:
      for temp,r in enumerate(i):
        in2[temp].append(r)

    for o in outs:
      for temp,r in enumerate(o):
        out[temp].append(r)

    
    for i,o in zip(in2,out):
      d.add_data(i,o)
    return d

  def delete_index(self,index):
    del self.data[self.indexes.index(index)]
    del self.indexes[self.indexes.index(index)]
  