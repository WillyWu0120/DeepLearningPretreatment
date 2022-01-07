import numpy as np

data = np.load("data.npz")
for key, value in data.items():
    print(key)
    print("-----------")
    print(value)
    np.savetxt("data" + key + ".csv", value)