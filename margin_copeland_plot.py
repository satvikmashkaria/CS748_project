from collections import defaultdict
from itertools import permutations
from itertools import combinations
import sys
import numpy as np
import random

sys.path.insert(1, './cswor')
import cswor

def gain_copeland(vote): return 2 if list(vote).index('1')<list(vote).index('2') else 0

n_voters = 50
# n_voters = int(sys.argv[2])
N = n_voters
# probs = [float(i) for i in sys.argv[2:]]
probs = [0.1, 0.2, 0.5, 0.7]
probs = [i/sum(probs) for i in probs]
probs=sorted(probs, reverse=True)
n_candidates = len(probs)

np.random.seed(int(sys.argv[1]))
random.seed(42)

data = np.array([np.random.choice(range(1, n_candidates+1), size = n_candidates, replace = False, p = probs).astype(str) for i in range(n_voters)])

print("Hash", data[0])

alpha    = 0.001
BB_alpha = 1
BB_beta = 1
t = np.arange(1, N+1)

candidates = [str(i) for i in range(1, n_candidates+1)]
pairwise_wins = defaultdict(list)
pairs = list(combinations(candidates, 2))
# pairs = list(permutations(candidates, 2))
# print(pairwise_wins)

for vote in data:
    vote = list(vote)
    # print(vote)
    for a, b in pairs:
        pairwise_wins[(a, b)].append(1 if vote.index(a) < vote.index(b) else 0)
        pairwise_wins[(b, a)].append(0 if vote.index(a) < vote.index(b) else 1)

pairwise_CIs = defaultdict(list)
for p in pairwise_wins:
	# print(pairwise_wins[p], p)
	output = cswor.BBHG_confseq(pairwise_wins[p], N, BB_alpha, BB_beta, alpha=alpha, running_intersection=True)
	pairwise_CIs[p] = output
	pairwise_CIs[(p[1], p[0])] = [N-i for i in output[1]], [N-i for i in output[0]]

print("pairwise", pairwise_CIs[('1', '2')])

bounds = defaultdict(list)
for i in range(N):
    for c in candidates:
        wins, losses = 0, 0
        for c2 in candidates:
            if (c, c2) in pairwise_CIs:
                if pairwise_CIs[(c, c2)][0][i] > N/2: wins+=1
                if pairwise_CIs[(c, c2)][1][i] < N/2: losses+=1
        ties = (n_candidates-1) - wins - losses
        bounds[c+'l'].append(wins-losses-ties)
        bounds[c+'u'].append(wins-losses+ties)

separate = N
print(bounds)

for i in range(N):
    if bounds['1l'][i] > bounds['2u'][i]: separate = min(separate, i)

print(N, separate)
# gains = sorted([gain_copeland(v) for v in data])
# margin = pairwise_wins[('1', '2')].count(1) - pairwise_wins[('2', '1')].count(1)
# while margin>0: margin-=gains.pop()

# print(probs[0]*probs[1], (len(data)-len(gains))/N, N, separate)
# print(pairwise_wins[('1', '2')].count(1), pairwise_wins[('2', '1')].count(1), pairwise_wins[('1', '2')].count(1) - pairwise_wins[('2', '1')].count(1), )