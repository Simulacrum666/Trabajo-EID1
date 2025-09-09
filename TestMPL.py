# Crea un archivo test_matplotlib.py
#update 1.1
import matplotlib.pyplot as plt
import numpy as np

x = np.array([1, 2, 3, 4, 5])
y = np.array([1, 0, 2, -3, 10])

plt.plot(x, y)
plt.show()
