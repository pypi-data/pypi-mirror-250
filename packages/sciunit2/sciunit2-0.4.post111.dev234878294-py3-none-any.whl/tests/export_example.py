import numpy as np
import requests
import os
print('cwd is: ' + os.getcwd())
r = requests.get('https://python.org')
print('status_code: ', r.status_code)
np_arr = np.array([1, 2, 3, 4, 5])
print('numpy array: ', np_arr)
