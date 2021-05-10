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
import random

sys.path.insert(1, '../cswor')
import cswor
importlib.reload(cswor)

plt.rc('text', usetex=False)
plt.rc('font', family='serif')
plt.rc('font', size=15)



alpha    = 0.001
N        = 1000
Ta_true  = 650
# Uniform prior
BB_alpha = 1
BB_beta  = 1
n = np.ones(N)

x = np.append(np.ones(Ta_true), np.zeros(N - Ta_true))
np.random.shuffle(x)
t = np.arange(1, len(x) + 1)

DM_x = np.zeros((3, N))

for i in range(N):
    r = random.randint(0, 2)
    DM_x[r][i] = 1

print(DM_x)
# exit(0)

CIs_lower_a, CIs_upper_a = cswor.BBHG_confseq(x, N, BB_alpha, BB_beta,
                                              alpha=alpha,
                                              running_intersection=True)

CIs_lower_a = np.array(CIs_lower_a)
CIs_upper_a = np.array(CIs_upper_a)

CIs_lower_b = N - CIs_upper_a
CIs_upper_b = N - CIs_lower_a
# Create confidence sequence plots
plt.figure(figsize=(7, 4))
plt.fill_between(t, CIs_lower_a, CIs_upper_a, color='tab:green',
                 label = "Green", alpha =0.3)
plt.fill_between(t, CIs_lower_b, CIs_upper_b, color='tab:red',
                 linestyle='--', lw=2,
                 label = "Red", alpha = 0.3)
plt.axhline(Ta_true, color='tab:green', linestyle='-.', )
plt.axhline(N-Ta_true, color='tab:red', linestyle='-.', )
# Add vertical line for when the audit can stop
plt.legend(loc = "best")

stopping_time = np.where(CIs_lower_a > N/2)[0][0]
plt.vlines(x = stopping_time,
           color="grey", ymin=-10, ymax=500,
           linestyle = ":")
plt.text(x = stopping_time + 10,
         y = 100, s = str(stopping_time) + " samples")

plt.ylim(-10, 1010)
plt.xlabel("Balls sampled from the urn")
plt.ylabel("Number of balls in the urn")
# plt.tight_layout()
plt.show()
plt.savefig("../figures/twoPartyConfseq.png")