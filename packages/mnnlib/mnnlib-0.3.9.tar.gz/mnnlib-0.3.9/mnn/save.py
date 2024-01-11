from mnn import network


class save: 
  """
  saves the network to a mnn model file
  """
  def __init__(self,net:network):
    self.net = net


  def save(self,file_name:str):
    """
    saves to a file
    """
    layers = self.net.layers
    out = ""
    for l in layers:
      out += f"{l.inp_count},{l.out_count}\n"
      for n in l.neurons:
        out += f" {n.activation.__name__}\n"
        for w in n.weights:
          out += f"  {w.weight}\n"
    with open(file_name,"w") as f:
      f.write(out)