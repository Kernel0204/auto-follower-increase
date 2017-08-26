#-*-coding:utf-8-*-
import numpy as np
import matplotlib.pyplot as plt

follower = np.arange(10000)
e = follower ** float(-1/5)
plt.plot(follower,e)
plt.show()
