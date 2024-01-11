class dataset:
  """
  class that holds data for the network
  """
  def __init__(self):
    self.inps = []
    self.outs = []
    self.count = 0

  def add_data(self,inp,out):
    """
    adds data to the dataset
    """
    self.inps.append(inp)
    self.outs.append(out)


  def get_next(self):
    """
    get the next data point
    """
    temp =  (self.inps[self.count],self.outs[self.count])
    self.count += 1
    return temp

  def reset(self):
    self.count = 0