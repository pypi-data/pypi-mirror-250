from mnn.neuron import neuron


class layer:

  """
  one layer of the network
  contains variable amount of neurons
  """

  def __init__(self, input_count:int, output_count:int, act_func):
    self.inp_count = input_count
    self.out_count = output_count
    self.neurons = []
    for _ in range(output_count):
      self.neurons.append(neuron(input_count, act_func))

  def __str__(self):
    t = f"neuron count: {len(self.neurons)}"
    return t

  def get_weights(self):
    """
    returns all weights in the layer
    """
    weights = []
    for n in self.neurons:
      weights += n.get_weights()
    return weights

  def run(self, input):
    """
    gets the output for the layer based on the input
    """
    temp = []
    for n in self.neurons:
      temp.append(n.run(input))
    return temp
