# Author: Laura Kulowski

'''

Generate a synthetic dataset for our LSTM encoder-decoder
We will consider a noisy sinusoidal curve 

'''

import numpy as np 

def synthetic_data(Nt = 2000, tf = 80 * np.pi):
    
    '''
    create synthetic time series dataset
    : param Nt:       number of time steps (float)
    : param tf:       final time (float)
    : return t, y:    time, feature (arrays)
    '''
    
    t = np.linspace(0., tf, Nt)
    y = np.sin(2. * t) + 0.3 * np.sin(1. * t) + 0.5 * np.cos(t) + 1.2 * np.cos(0.5 * t + 0.2) + np.random.normal(0., 0.05, Nt)

    return t, y

def train_test_split(t, y, split = 0.8):

  '''
  
  split time series into train/test sets
  
  : param t:                      time (array) 
  : para y:                       feature (array)
  : para split:                   percent of data to include in training set (float)
  : return t_train, y_train:      time/feature training and test sets;  
  :        t_test, y_test:        (shape: [# samples, 1])
  
  '''
  
  indx_split = int(split * len(y))
  indx_train = np.arange(0, indx_split)
  indx_test = np.arange(indx_split, len(y))
  
  t_train = t[indx_train]
  y_train = y[indx_train]
  y_train = y_train.reshape(-1, 1)
  
  t_test = t[indx_test]
  y_test = y[indx_test]
  y_test = y_test.reshape(-1, 1)
  
  return t_train, y_train, t_test, y_test 


def windowed_dataset(y, input_window = 5, output_window = 1, stride = 1, num_features = 1):
  
    '''
    create a windowed dataset
    
    : param y:                time series feature
    : param input_window:     number of y samples to give model 
    : param output_window:    number of future y samples to predict  
    : param stide:            spacing between windows   
    : param num_features:     number of features (i.e., 1 for us, but we could have multiple features)
    : return X, Y:            arrays with correct dimensions for LSTM (i.e., [# samples, time steps, # features])
    '''
  
    L = y.shape[0]
    num_samples = (L - input_window - output_window) // stride + 1

    X = np.zeros([input_window, num_samples, num_features])
    Y = np.zeros([output_window, num_samples, num_features])    
    
    for ff in np.arange(num_features):
        for ii in np.arange(num_samples):
            start_x = stride * ii
            end_x = start_x + input_window
            X[:, ii, ff] = y[start_x:end_x, ff]

            start_y = stride * ii + input_window
            end_y = start_y + output_window 
            Y[:, ii, ff] = y[start_y:end_y, ff]

    return X, Y
