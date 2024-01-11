from mnn.utils import mult_lists
from mnn.weight import weight
from random import uniform


class neuron():

  """
  one neuron in the network
  """

  def __init__(self, inp_count:int, act_func):
    self.weights = []
    self.activation = act_func
    for _ in range(inp_count):
      self.weights.append(weight(uniform(-1.0, 1.0)))
    self.inp_count = inp_count
    # self.bias = weight(uniform(-1.0, 1.0))

  def run(self, input):
    """
    runs the input through the neuron
    returns the output of the neuron
    """
    w_l = [w.get_weight() for w in self.weights]
    temp = mult_lists(input, w_l)
    temp = sum(temp)
    # temp += self.bias.get_weight()
    temp = self.activation(inp=temp)
    return temp

  def get_weights(self):
    """
    returns all of the weights in the neuron
    """
    temp = self.weights
    # temp.append(self.bias)
    
    return temp
