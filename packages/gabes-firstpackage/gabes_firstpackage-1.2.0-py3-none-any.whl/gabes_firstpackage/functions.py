from .__init__ import *
from sklearn.metrics import roc_auc_score

class Func():
  
  def sigmoid(X):
    return (1/(1+np.exp(-X)))
  
  def der_sigmoid(X):
    sigma = Func.sigmoid(X)
    return (sigma*(1 - sigma))
  
  def der_tanh(X):
    return np.cosh(X)**-2
  
  def ReLU(X):
    return (X + abs(X))/2
  
  def der_ReLU(X):
    return (X > 0) * 1
  
  def sinc(X):
    return np.sin(X)/X
  
  def der_sinc(X):
    return (X*np.cos(X) - np.sin(X))/X**2
  
  def x_squared(X):
    return X**2
  
  def der_x_squared(X):
    return 2*X
  
  def mse(x, y):
    x, y = Func.reshape_input(x, y)
    return sum((x - y)**2)/y.shape[0]
  
  def acc(x, y):
    x, y = Func.reshape_input(x, y)
    return sum(((x >= .5)*1 == y)*1)

  def roc_auc(x, y):
    return roc_auc_score(y, x)

  def log_loss(x, y):
    x, y = Func.reshape_input(x, y)
    return -np.squeeze(sum(y*np.log(x)
                           + (1 - y)*np.log1p(-x)))/len(y)

  def reshape_input(x, y):
    return [np.array(x).reshape(-1), np.array(y).reshape(-1)]   

    