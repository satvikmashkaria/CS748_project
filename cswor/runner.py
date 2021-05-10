from mod_copeland import sample_complexity


args = {}
# args['heuristic'] = 'random'
args['heuristic'] = 'greedy'
args['n_voters'] = 1000
args['alpha'] = 0.05
# args['probs'] = [0.4, 0.45, 0.5, 0.7, 0.8]
# args['probs'] = [0.1, 0.2, 0.3, 0.4, 0.5]
args['probs'] = [0.1 + 0.05*i for i in range(10)]
print("ppp", args['probs'])
args['seed'] = 42
args['ques_limit'] = 5
gammas = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
# gammas = [0.0]
greedy_itrs = []
random_itrs = []
seeds = [2, 3, 4]
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
#     for gamma in gammas:
#         print("Gamma", gamma, "started")
#         args['gamma'] = gamma
#         itr, winner = sample_complexity(args)
#         print("seed", seed, "itr", itr, "winner", winner)
#         seed_vals.append(itr)
#     greedy_itrs.append(seed_vals)
# #
# print(greedy_itrs)
# print(sample_complexity(args))


greedy_itrs = [[257, 307, 377, 424, 297, 453], [252, 303, 377, 424, 297, 453], [251, 307, 377, 424, 297, 453], [254, 307, 377, 424, 297, 453], [254, 307, 377, 424, 297, 453], [254, 307, 377, 424, 297, 453]]

print([sum(i)/6 for i in greedy_itrs])

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()

# plt.plot(gammas, [sum(i)/6 for i in greedy_itrs])
# plt.xlabel("Gamma")
# plt.ylabel("Average sample complexity")
# plt.title("Variation with Gamma")
# plt.show()

res = [[649, 496, 496, 496, 496, 496], [565, 496, 496, 496, 496, 496], [524, 747, 782, 526, 526, 526]]

def suml(l1, l2):
    return [(l1[i] + l2[i]) for i in range(len(l1))]

resf = suml(suml(res[0], res[1]), res[2])
resf = [i/3 for i in resf]

import matplotlib.pyplot as plt

plt.plot(gammas, resf)
plt.xlabel("Gamma Values")
plt.ylabel("Sample complexity averaged over 3 seeds")
plt.savefig("gamma_variation.png")
plt.show()