import scipy.stats
import numpy as np
import matplotlib.pyplot as plt

data = [0.9211063385009766, 0.8273544311523438, 0.8892269134521484, 0.90447998046875, 0.8740768432617188, 0.9287176132202148, 
0.9086589813232422, 0.9211130142211914, 0.9615898132324219, 0.9213066101074219, 0.8382635116577148, 0.8449916839599609, 
0.8565073013305664, 0.8775672912597656, 0.823124885559082, 0.9001426696777344, 0.8820638656616211, 0.8232526779174805]

counts, start, dx, _ = scipy.stats.cumfreq(data, numbins=20)
x = np.arange(counts.size) * dx + start

plt.plot(x, counts, 'ro')
plt.xlabel('Value')
plt.ylabel('Cumulative Frequency')

plt.show()

data = [0.9173097610473633, 0.8310298919677734, 0.8933639526367188, 0.9010915756225586, 0.8085269927978516, 0.906982421875, 
0.9283857345581055, 0.8950767517089844, 0.9095001220703125, 0.9225835800170898, 0.8077592849731445, 0.8313884735107422, 
0.8217363357543945, 0.8373317718505859, 0.8653907775878906, 0.9032487869262695, 0.8546609878540039, 0.8301258087158203]

counts, start, dx, _ = scipy.stats.cumfreq(data, numbins=20)
x = np.arange(counts.size) * dx + start

plt.plot(x, counts, 'ro')
plt.xlabel('Value')
plt.ylabel('Cumulative Frequency')

plt.show()