class weight:

  """
  one weight in the network
  """
  def __init__(self,weight:float):
    self.weight = weight

  def get_weight(self):
    """
    returns the weight
    """
    return self.weight

  def __str__(self):
    return f"weight: {self.weight}"
