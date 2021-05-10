import sys
import numpy as np
# np.random.seed(int(sys.argv[1]))
import matplotlib.pyplot as plt
import math


sys.path.insert(1, './cswor')
import cswor_my as cswor

def gain_approval(vote): return int('1' in vote) + int('2' not in vote)

n_voters = 1000
N = n_voters
# probs = [float(i) for i in sys.argv[2:]]
# probs = [i/sum(probs) for i in probs]
# probs=sorted(probs, reverse=True)

# probs = [0.6, 0.2, 0.1, 0.1]
# n_candidates = len(probs)
#
# data = []
# while len(data) < n_voters:
#     vote = []
#     for i in range(n_candidates):
#         if np.random.binomial(1, probs[i]): vote.append(str(i+1))
#     if vote and len(vote)<n_candidates: data.append(vote)

# print(data)
# exit(0)
# print()
alphas = [1e-5, 5e-5, 1e-4, 5e-4, 1e-3, 5e-3, 1e-2, 5e-2]
seeds = range(1)
np.random.seed(1)
epss = [0.05, 0.1, 0.15, 0.2, 0.24]
epss = [0.2]
# epss = [i/100 for i in range(1, 24)]
print(epss)
# exit(0)
slopes = []
for eps in epss:
    probs = [0.25 + 2*eps, 0.25, 0.25 - eps, 0.25 - eps]
    print(probs)
    n_candidates = len(probs)
    seeds = range(1)
    SLOPE_SUM = 0
    for seed in seeds:
        np.random.seed(seed)
        data = []
        while len(data) < n_voters:
            vote = []
            for i in range(n_candidates):
                if np.random.binomial(1, probs[i]): vote.append(str(i + 1))
            if vote and len(vote) < n_candidates: data.append(vote)
        seps = []

        for alpha in alphas:
            # alpha    = 0.001
            BB_alpha = 1
            BB_beta = 1
            t = np.arange(1, N+1)

            xs = np.zeros((n_candidates, n_voters))
            for i, vote in enumerate(data):
                for voted in vote: xs[int(voted)-1][i] = 1


            CIs_lower_a1, CIs_upper_a1 = cswor.BBHG_confseq(xs[0], N, BB_alpha, BB_beta, alpha=alpha, running_intersection=True)
            CIs_lower_a2, CIs_upper_a2 = cswor.BBHG_confseq(xs[1], N, BB_alpha, BB_beta, alpha=alpha, running_intersection=True)

            separate = N

            for i in range(N):
                if CIs_lower_a1[i] > CIs_upper_a2[i]: separate = min(separate, i)

            gains = sorted([gain_approval(v) for v in data])
            margin = list(xs[0]).count(1)-list(xs[1]).count(1)
            while margin>0: margin-=gains.pop()
            seps.append(separate)
            print(alpha, (probs[0]-probs[1])/2, (len(data)-len(gains))/N, separate)
        # plt.plot([-math.log10(i) for i in alphas], seps, label="Epsilon=" + str(eps))
        plt.plot([1 - i for i in alphas], seps, label="Epsilon=" + str(eps))
        slope_temp = (seps[0] - seps[-1])/(math.log10(alphas[0]) - math.log10(alphas[-1]))
        SLOPE_SUM += slope_temp
        print(seps)
    slopes.append(SLOPE_SUM/5)

print(slopes)
plt.xlabel("log(1/delta)")
plt.ylabel("sample complexity")
plt.title("Variation with delta")
plt.legend()
plt.savefig("var_delta_new.png")
plt.show()
# print(data)
# print(CIs_lower_a1)
# print(CIs_upper_a2)

[]