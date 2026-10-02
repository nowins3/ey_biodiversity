import numpy as np
import pandas as pd
X = np.load('temporal_train.npy')
X = X.transpose((0, 2, 1))
print(X[306][0])
print(X[1385][0])