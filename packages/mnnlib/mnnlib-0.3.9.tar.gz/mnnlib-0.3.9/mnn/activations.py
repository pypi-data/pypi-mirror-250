import math

#just activation functions
#they are passed as a paramater to the layers

def relu(inp:float):
  """
  Basic rectified linear unit (relu) activation function
  works for most basic networks
  if x < 0 : return 0
  else return x
  """
  __name__ = "relu"
  if inp < 0:
    return 0
  else:
    return inp


def sigmoid(inp:float):
  """
  Sigmoid activation function
  good for having negative numbers
  and for more complex networks
  """
  __name__ = "sigmoid"
  return 1 / (1 + math.exp(-inp))


def straight(inp:float):

  """
  Straight activation function
  very basic
  just returns the input
  good for simple networks
  """
  
  __name__ = "straight"
  return inp


def binary(inp:float):
  """
  binary activation function
  if x > 0 : return 1
  else return 0
  good for binary classification
  """
  __name__ = "binary"
  if inp <= 0:
    return 0
  else:
    return 1


def leakyrelu(inp:float):
  """
  Leaky relu activation function
  in most cases better than relu
  """
  __name__ = "leakyrelu"
  if inp < 0:
    return inp * 0.01
  else:
    return inp
