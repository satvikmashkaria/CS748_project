import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.lines import Line2D
from matplotlib import rcParams
# from IPython.display import HTML
import numpy as np
import importlib
import math
from scipy.special import comb
import sys
import time

sys.path.insert(1, '../cswor')
import cswor
importlib.reload(cswor)

plt.rc('text', usetex=False)
plt.rc('font', family='serif')
plt.rc('font', size=15)


alpha    = 0.001
R        = 300
G        = 150
P        = 50
N = R + G + P
# Uniform prior
DM_alpha = [1, 1, 1]
K = len(DM_alpha)
n = np.ones(N)

R_votes = np.array([[1, 0, 0], ] * R).T
G_votes = np.array([[0, 1, 0], ] * G).T
P_votes = np.array([[0, 0, 1], ] * P).T

votes   = np.column_stack((R_votes, G_votes, P_votes))
np.random.shuffle(votes.T)

votes_cumsum = votes.cumsum(axis = 1)

# MLE at each time: N * x_cumsum / intrinsic_time
intrinsic_time = votes_cumsum.sum(axis = 0)
T_hats = np.transpose(N * 
                  np.divide(votes_cumsum,
                            intrinsic_time[None, :]))

# Create confidence set sequence plots
c3d = cswor.Confseq3D(votes, N, DM_alpha, alpha, fineness = 1)

samples = [20, 20, N] 

# cs1 = c3d.update_from_S_t(samples[0])
# cs2 = c3d.update_from_S_t(samples[1])
cs3 = c3d.update_from_S_t(samples[2])

# fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize = (10, 3.5))
# ax1.imshow(cs1, 
#            interpolation = 'none', extent = [0, N, N, 0])
# ax1.set_title(str(samples[0]) + " samples")
# ax2.imshow(cs2, 
#            interpolation = 'none', extent = [0, N, N, 0])
# ax2.set_title(str(samples[1]) + " samples")
# ax2.axes.get_yaxis().set_visible(False)
# ax3.imshow(cs3, 
#            interpolation = 'none', extent = [0, N, N, 0])
# ax3.set_title(str(samples[2]) + " samples")
# ax3.axes.get_yaxis().set_visible(False)

# ax1.set(ylabel = 'Total red balls')
# ax2.set(xlabel = 'Total green balls')

# s = 6

# ax1.scatter(R, G, label = "True total",
#             s = s, color = "tab:blue")
# ax2.scatter(R, G, label = "True total",
#             s = s, color = "tab:blue")
# ax3.scatter(R, G, label = "True total",
#             s = s, color = "tab:blue")
# ax3.legend(loc = "best")

# plt.setp((ax1, ax2, ax3), xlim=(0, N+1), ylim=(0, N+1))
# plt.show()
