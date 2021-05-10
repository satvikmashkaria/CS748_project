from mod_copeland_yateesh import sample_complexity


args = {}
# args['heuristic'] = 'random'
args['heuristic'] = 'greedy'
# args['heuristic'] = 'mod_dcb'
args['n_voters'] = 4639
args['alpha'] = 0.05
args['seed'] = 42
args['ques_limit'] = 5
args['gamma'] = 0.5
args['probs'] = [0.05, 0.1, 0.2, 0.4]
q_limits = [1, 2, 3, 5, 8, 10, 13, 15, 20, 25, 30]
# q_limits = [1]
# gammas = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
# gammas = [0.0]
greedy_itrs = []
random_itrs = []
seeds = [0, 1, 2, 3, 4]
# seeds = [0]

# for seed in seeds:
#     args['seed'] = seed
#     itr, winner = sample_complexity(args)
#     print("seed", seed, "itr", itr, "winner", winner)
#     random_itrs.append(itr)
#
# print(random_itrs)
# print(sum(random_itrs)/6)

# for seed in seeds:
#     seed_vals = []
#     args['seed'] = seed
#     for q_limit in q_limits:
#         args['ques_limit'] = q_limit
#         print("Que. limit ", q_limit, "started")
#         itr, winner = sample_complexity(args)
#         print("seed", seed, "itr", itr, "winner", winner)
#         seed_vals.append(itr)
#     greedy_itrs.append(seed_vals)
# ###
# print(greedy_itrs)
# print(sample_complexity(args))


greedy_itrs = [[283, 199, 167, 167, 167, 167, 167, 167, 167, 167, 167], [209, 160, 109, 93, 93, 93, 93, 93, 93, 93, 93], [216, 169, 112, 104, 104, 110, 104, 104, 104, 104, 104], [228, 124, 116, 116, 116, 116, 116, 116, 116, 116, 116], [479, 362, 363, 363, 362, 362, 363, 363, 363, 363, 363]]
dcb_itrs = [[499, 373, 343, 170, 180, 179, 180, 180, 180, 180, 180], [893, 714, 660, 546, 547, 468, 340, 79, 79, 79, 79], [672, 298, 231, 201, 207, 180, 166, 169, 169, 169, 169], [940, 432, 310, 310, 116, 175, 194, 198, 198, 198, 198], [481, 523, 357, 352, 446, 365, 346, 345, 345, 345, 345]]
dcb_mod_itrs = [[589, 385, 183, 157, 168, 168, 175, 179, 178, 175, 174], [711, 558, 553, 469, 427, 299, 291, 57, 117, 119, 118], [454, 349, 267, 214, 168, 168, 165, 153, 103, 72, 103], [648, 440, 302, 310, 117, 120, 181, 180, 198, 197, 28], [564, 364, 448, 361, 345, 447, 363, 56, 345, 345, 345]]

import numpy as np
import matplotlib.pyplot as plt

def convert(lst):
    lst = [np.array(i) for i in lst]
    lst = sum(lst)
    lst = [i/5 for i in lst]
    return lst
print(convert(greedy_itrs))
print(convert(dcb_itrs))
print(convert(dcb_mod_itrs))

import seaborn as sns
sns.set_theme()

plt.plot(q_limits, convert(greedy_itrs), label="Greedy (ours)")
# plt.plot(q_limits, convert(dcb_itrs), label="DCB")
plt.plot(q_limits, convert(dcb_mod_itrs), label="DCB Extended")

plt.xlabel("Num of questions asked")
plt.ylabel("Avg sample complexity")
plt.title("US election 2012 data (16 candidates)")
plt.legend()
plt.savefig("us_comp.png")
plt.show()

# greedy_itrs = [[257, 307, 377, 424, 297, 453], [252, 303, 377, 424, 297, 453], [251, 307, 377, 424, 297, 453], [254, 307, 377, 424, 297, 453], [254, 307, 377, 424, 297, 453], [254, 307, 377, 424, 297, 453]]
#
# print([sum(i)/6 for i in greedy_itrs])
#
# import matplotlib.pyplot as plt
#
# plt.plot(gammas, [sum(i)/6 for i in greedy_itrs])
# plt.xlabel("Gamma")
# plt.ylabel("Average sample complexity")
# plt.show()

# res = [[649, 496, 496, 496, 496, 496], [565, 496, 496, 496, 496, 496], [524, 747, 782, 526, 526, 526]]
#
# def suml(l1, l2):
#     return [(l1[i] + l2[i]) for i in range(len(l1))]
#
# resf = suml(suml(res[0], res[1]), res[2])
# resf = [i/3 for i in resf]
#
# import matplotlib.pyplot as plt
#
# plt.plot(gammas, resf)
# plt.xlabel("Gamma Values")
# plt.ylabel("Sample complexity averaged over 3 seeds")
# plt.show()