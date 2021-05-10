import matplotlib.pyplot as plt
import sys
import numpy as np

sys.path.insert(1, '../cswor')
import cswor
N = 1000

def get_intervals(np_array):
    max1, min1 = float('-inf'), float('inf')
    max2, min2 = float('-inf'), float('inf')
    max3, min3 = float('-inf'), float('inf')
    for i in range(len(np_array)):
        for j in range(len(np_array[0])):
            if np_array[i][j]:
                # print(i, j)
                max1, min1 = max(max1, j*2), min(min1, j*2)
                max2, min2 = max(max2, i*2), min(min2, i*2)
                max3, min3 = max(max3, N-i*2-j*2), min(min3, N-i*2-j*2)
    if max1==float('-inf'): max1 = N
    if max2==float('-inf'): max2 = N
    if max3==float('-inf'): max3 = N
    if min1==float('inf'): min1 = 0
    if min2==float('inf'): min2 = 0
    if min3==float('inf'): min3 = 0
    return ((min1, max1), (min2, max2), (min3, max3))

def get_borda_l(CIs):
    if N - CIs[0][0] - CIs[1][0] < CIs[2][1]: return CIs[0][0]*2 + CIs[1][0] + N
    if N - CIs[0][0] - CIs[2][1] < CIs[1][1]: return CIs[0][0]*2 + (N - CIs[2][1] - CIs[0][0]) + N
    return (N - CIs[1][1] - CIs[2][1])*2 + CIs[1][1] + N

def get_borda_u(CIs):
    if N - CIs[1][0] - CIs[1][0] < CIs[0][1]: return (N - CIs[1][0] - CIs[2][0])*2 + CIs[1][0] + N
    if N - CIs[0][1] - CIs[2][0] < CIs[1][1]: return CIs[0][1]*2 + (N - CIs[0][1] - CIs[2][0]) + N
    return CIs[0][1]*2 + CIs[1][1] + N

bc_l1, bc_u1 = [], []
bc_l2, bc_u2 = [], []
bc_l3, bc_u3 = [], []

# CI_l_1, CI_u_1 = [], []
# CI_l_2, CI_u_2 = [], []
# CI_l_3, CI_u_3 = [], []
# for sample in range(5, N, 5):
#     o = get_intervals(np.load('run_3_3/'+str(sample)+'_1.npy'))
#     CI_l_1.append(o[0][0])
#     CI_u_1.append(o[0][1])
#     CI_l_2.append(o[1][0])
#     CI_u_2.append(o[1][1])
#     CI_l_3.append(o[2][0])
#     CI_u_3.append(o[2][1])
#     bc_l1.append(get_borda_l(o))
#     bc_u1.append(get_borda_u(o))

# CI_l_1, CI_u_1 = [], []
# CI_l_2, CI_u_2 = [], []
# CI_l_3, CI_u_3 = [], []
# for sample in range(5, N, 5):
#     o = get_intervals(np.load('run_3_3/'+str(sample)+'_2.npy'))
#     CI_l_1.append(o[0][0])
#     CI_u_1.append(o[0][1])
#     CI_l_2.append(o[1][0])
#     CI_u_2.append(o[1][1])
#     CI_l_3.append(o[2][0])
#     CI_u_3.append(o[2][1])
#     bc_l2.append(get_borda_l(o))
#     bc_u2.append(get_borda_u(o))

# CI_l_1, CI_u_1 = [], []
# CI_l_2, CI_u_2 = [], []
# CI_l_3, CI_u_3 = [], []
for sample in range(5, N, 5):
    o = get_intervals(np.load(str(sample)+'_1.npy'))
    # CI_l_1.append(o[0][0])
    # CI_u_1.append(o[0][1])
    # CI_l_2.append(o[1][0])
    # CI_u_2.append(o[1][1])
    # CI_l_3.append(o[2][0])
    # CI_u_3.append(o[2][1])
    bc_l3.append(get_borda_l(o))
    bc_u3.append(get_borda_u(o))

# t = list(range(5, N, 5))
print(bc_l3)
print(bc_u3)
# plt.figure()
# plt.fill_between(t, bc_l1, bc_u1, color='tab:green', label = "Green", alpha =0.3)
# plt.fill_between(t, bc_l2, bc_u2, color='tab:red', label = "Red", alpha =0.3)
# plt.fill_between(t, bc_l3, bc_u3, color='tab:blue', label = "Blue", alpha =0.3)
# plt.show()

# plt.figure()
# plt.fill_between(t, CI_l_1, CI_u_1, color='tab:green', label = "Green", alpha =0.3)
# plt.fill_between(t, CI_l_2, CI_u_2, color='tab:red', label = "Red", alpha =0.3)
# plt.fill_between(t, CI_l_3, CI_u_3, color='tab:blue', label = "Blue", alpha =0.3)
# plt.show()

# print(CI_l_1)
# print(CI_u_1)
# print(CI_l_2)
# print(CI_u_2)
# print(CI_l_3)
# print(CI_u_3)

# print(get_intervals(np.load('run_3/0.npy')))
# print(get_intervals(np.load('run_3/100.npy')))
# print(get_intervals(np.load('run_3/200.npy')))
# print(get_intervals(np.load('run_3/300.npy')))
# print(get_intervals(np.load('run_3/400.npy')))
# print(get_intervals(np.load('run_3/500.npy')))
# print(get_intervals(np.load('run_3/600.npy')))
# print(get_intervals(np.load('run_3/700.npy')))
# print(get_intervals(np.load('run_3/800.npy')))
# print(get_intervals(np.load('run_3/900.npy')))
# print(get_intervals(np.load('run_3/1000.npy')))