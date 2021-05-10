import importlib
import numpy as np
import sys

sys.path.insert(1, './cswor')
import cswor
importlib.reload(cswor)

alpha    = 0.05 
N        = 1000
Ta_true  = 650
step = 670
# Uniform prior
BB_alpha = 1
BB_beta  = 1
n = np.ones(N)

x = np.append(np.ones(Ta_true), np.zeros(N - Ta_true))
np.random.shuffle(x)
# x = np.array([4, 1])
t = np.arange(1, len(x) + 1)
# t = np.array([6, 7])
import time
s = time.time()
CIs_lower_a, CIs_upper_a = cswor.BBHG_confseq(x, N, BB_alpha, BB_beta,
                                              alpha=alpha,
                                              running_intersection=True, times=np.arange(0, N, step=1))
# print('Final', CIs_lower_a, CIs_upper_a)
# print('Final', CIs_lower_a[::10], CIs_upper_a[::10])
# print('Final', CIs_lower_a[10::10], CIs_upper_a[10::10])
print('Final', CIs_lower_a[step-3:step+3], CIs_upper_a[step-3:step+3])

print(time.time()-s)

# CIs_lower_a, CIs_upper_a = cswor.BBHG_confseq(x, N, BB_alpha, BB_beta,
#                                               alpha=alpha,
#                                               running_intersection=True, times=np.arange(0, N, step=10))
# print('Final', CIs_lower_a, CIs_upper_a)

s=time.time()
start, end = 0, N
CIs_lower_a, CIs_upper_a = cswor.BBHG_confseq(x, N, BB_alpha, BB_beta,
                                              alpha=alpha,
                                              running_intersection=True, times=np.array([0, step, step+1, N-1]), start=start, end=end)
print('Final', CIs_lower_a, CIs_upper_a)
print(time.time()-s, start, end)

s=time.time()
start, end = 100, 900
CIs_lower_a, CIs_upper_a = cswor.BBHG_confseq(x, N, BB_alpha, BB_beta,
                                              alpha=alpha,
                                              running_intersection=True, times=np.array([0, step, step+1]), start=start, end=end)
print('Final', CIs_lower_a, CIs_upper_a)
print(time.time()-s, start, end)

s=time.time()
start, end = 200, 800
CIs_lower_a, CIs_upper_a = cswor.BBHG_confseq(x, N, BB_alpha, BB_beta,
                                              alpha=alpha,
                                              running_intersection=True, times=np.array([0, step]), start=start, end=end)
print('Final', CIs_lower_a, CIs_upper_a)
print(time.time()-s, start, end)

s=time.time()
start, end = 300, 700
CIs_lower_a, CIs_upper_a = cswor.BBHG_confseq(x, N, BB_alpha, BB_beta,
                                              alpha=alpha,
                                              running_intersection=True, times=np.array([0, step]), start=start, end=end)
print('Final', CIs_lower_a, CIs_upper_a)
print(time.time()-s, start, end)

s=time.time()
start, end = 600, 700
CIs_lower_a, CIs_upper_a = cswor.BBHG_confseq(x, N, BB_alpha, BB_beta,
                                              alpha=alpha,
                                              running_intersection=True, times=np.array([0, step, step+1, N-1]), start=start, end=end)
print('Final', CIs_lower_a, CIs_upper_a)
print(time.time()-s, start, end)