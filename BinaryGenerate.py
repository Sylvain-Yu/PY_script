import numpy as np


a = np.array([585,2],dtype="float32")
a.dtype = np.uint32
a.byteswap(True)
print(hex(a[0]))