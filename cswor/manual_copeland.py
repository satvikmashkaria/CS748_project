import numpy as np
from collections import defaultdict
from itertools import combinations


# data = np.load("../US_data_clean.npy")
n_voters = 1000
n_candidates = 10
probs = [0.1 for i in range(10)]

for seed in range(10):
    np.random.seed(seed)
    print("seed is ", seed)
    data = np.array([np.random.choice(range(1, n_candidates + 1), size=n_candidates, replace=False, p=probs).astype(str) for i in range(n_voters)])


    N, num_candidates = data.shape
    # print(N, num_candidates)

    candidates = [str(i+1) for i in range(num_candidates)]
    pairwise_wins = defaultdict(int)
    # print(candidates)

    for i in range(N):
        vote = list(data[i])
        # print(vote)
        for a, b in combinations(candidates, 2):
            a, b = str(a), str(b)
            pairwise_wins[(a, b)] += (1 if vote.index(a) < vote.index(b) else 0)
            pairwise_wins[(b, a)] += (0 if vote.index(a) < vote.index(b) else 1)

    # print(pairwise_wins[('1', '2')], pairwise_wins[('2', '1')])

    total_wins = [0 for i in range(num_candidates)]

    for i, c1 in enumerate(candidates):
        temp = 0
        for c2 in candidates:
            if c2 != c1:
                if pairwise_wins[(c1, c2)] >= N/2:
                    total_wins[i] += 1

    one, two = 0, 0
    for i in range(len(data)):
        if data[i][0] == '1':
            one += 1
        elif data[i][0] == '2':
            two += 1

    # print(one, two)

    print(total_wins, sum(total_wins))
    print("Winner is candidate: ", np.argmax(np.array(total_wins)) + 1)

