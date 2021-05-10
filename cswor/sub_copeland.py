from collections import defaultdict
from itertools import permutations
from itertools import combinations
import sys
import numpy as np
# np.random.seed(int(sys.argv[1]))
# sys.path.insert(1, './cswor')
import cswor
import random
import tqdm


def winner(pairwise_CIs):
    global candidates, already_decided

    # pairwise_CIs = defaultdict(list) ##
    # candidates = list(map(str, list(range(4)))) ##
    bounds = {}
    for c in candidates:
        wins, losses = 0, 0
        for c2 in candidates:
            if (c, c2) in pairwise_CIs:
                if pairwise_CIs[(c, c2)][0] > N/2:
                    wins += 1
                    already_decided[(c, c2)] = 1

                if pairwise_CIs[(c, c2)][1] < N/2:
                    losses += 1
                    already_decided[(c, c2)] = 1
        ties = (n_candidates-1) - wins - losses
        bounds[c+'l'] = wins-losses-ties
        bounds[c+'u'] = wins-losses+ties

    # print(bounds)

    for c in candidates:
        is_winner = True
        for c2 in candidates:
            if c2!=c and bounds[c+'l'] <= bounds[c2+'u']: is_winner = False
        if is_winner: return c
    return None

def random_heuristic(pairwise_CIs):

    global n_candidates, num_ques, candidates, already_decided

    combs = list(combinations(candidates, 2))
    combs = list(filter(lambda x: already_decided[x] != 1, combs))
    random.shuffle(combs)
    print(combs)
    kpairs = combs[:num_ques]
    return kpairs

def greedy_winner_heuristic(pairwise_CIs):

    global n_candidates, num_ques, candidates, already_decided, N

    scores = defaultdict(list)

    for (a, b) in pairwise_CIs:
        [lb, ub] = pairwise_CIs[(a, b)]
        scores[(a, b)] = (abs(ub - N/2) - abs(N/2 - lb))/(ub - lb + 1e-4)

    winning_probs = {}

    for c in candidates:
        wp = 0
        for c1 in candidates:
            if (c, c1) in scores:
                wp += scores[(c, c1)]
        winning_probs[c] = wp

    impact = defaultdict(float)

    for (a, b) in pairwise_CIs:
        impact[(a, b)] = winning_probs[a] + winning_probs[b]

    # print("WPs", winning_probs)
    # print("scores", scores)
    # print("impact", impact)

    gamma = 0.0
    for (a, b) in scores:
        scores[(a, b)] = - gamma * abs(scores[(a, b)]) + (1 - gamma) * impact[(a, b)] / (2 * (n_candidates - 1))
    scores = sorted(scores.items(), key = lambda kv: -kv[1])
    selected = [i[0] for i in scores][0::2][:num_ques]
    selected = list(filter(lambda x: already_decided[x] != 1, selected))

    # print("Final score: ", scores)
    # print("selected", selected)

    return selected


if __name__ == "__main__":

    n_voters = 1000
    N = n_voters
    # probs = [float(i) for i in sys.argv[2:]]
    probs = [0.1, 0.2, 0.5, 0.7]
    probs = [i / sum(probs) for i in probs]
    probs = sorted(probs, reverse=True)
    n_candidates = len(probs)
    num_ques = 5
    np.random.seed(4)
    random.seed(4)

    data = np.array(
        [np.random.choice(range(1, n_candidates + 1), size=n_candidates, replace=False, p=probs).astype(str) for i in
         range(n_voters)])

    # print("Hash", data[0])

    alpha = 0.05
    BB_alpha = 1
    BB_beta = 1
    t = np.arange(1, N + 1)

    candidates = [str(i) for i in range(1, n_candidates + 1)]
    pairwise_wins = defaultdict(list)
    pairs = list(combinations(candidates, 2))
    # pairs = list(permutations(candidates, 2))
    # print(pairwise_wins)

    # for vote in data:
    #     vote = list(vote)
    #     # print(vote)
    #     for a, b in pairs:
    #         pairwise_wins[(a, b)].append(1 if vote.index(a) < vote.index(b) else 0)
    #         pairwise_wins[(b, a)].append(0 if vote.index(a) < vote.index(b) else 1)

    # history = []
    already_decided = defaultdict(list)
    pairwise_CIs = defaultdict(list)

    for i in tqdm.tqdm(range(N)):
        # print("voter: ", i)
        next_set = greedy_winner_heuristic(pairwise_CIs)
        # next_set = random_heuristic(pairwise_CIs)
        vote = list(data[i])
        # print("vote", vote)
        for a, b in next_set:
            a, b = str(a), str(b)
            pairwise_wins[(a, b)].append(1 if vote.index(a) < vote.index(b) else 0)
            pairwise_wins[(b, a)].append(0 if vote.index(a) < vote.index(b) else 1)

        for a, b in combinations(candidates, 2):
            pairwise_CIs[(a, b)] = [0, N]
            pairwise_CIs[(b, a)] = [0, N]

        for p in pairwise_wins:
            # print(pairwise_wins[p], p)
            output = cswor.BBHG_confseq(pairwise_wins[p], N, BB_alpha, BB_beta, alpha=alpha, running_intersection=True)
            pairwise_CIs[p] = [output[0][-1], output[1][-1]]
            # pairwise_CIs[(p[1], p[0])] = [N - i for i in output[1]], [N - i for i in output[0]]
            pairwise_CIs[(p[1], p[0])] = [N - output[1][-1], N - output[0][-1]]

        # print(pairwise_CIs[('1', '2')])
        if winner(pairwise_CIs):
            print("The winner is:", winner(pairwise_CIs), "Found in", i, "steps")
            break

        # print("pairwise", pairwise_CIs)

    exit(0)
    bounds = defaultdict(list)
    for i in range(N):
        for c in candidates:
            wins, losses = 0, 0
            for c2 in candidates:
                if (c, c2) in pairwise_CIs:
                    if pairwise_CIs[(c, c2)][0][i] > N / 2: wins += 1
                    if pairwise_CIs[(c, c2)][1][i] < N / 2: losses += 1
            ties = (n_candidates - 1) - wins - losses
            bounds[c + 'l'].append(wins - losses - ties)
            bounds[c + 'u'].append(wins - losses + ties)

    separate = N
    # print(bounds)

    for i in range(N):
        if bounds['1l'][i] > bounds['2u'][i]: separate = min(separate, i)

    print(N, separate)

# 3 candidates

# gamma = 1 -> 76 steps
# gamma = 0 -> 73 steps
# random -> 95 steps

# 4 candidates
#
# gamma = 0 -> 74 steps
# gamma = 1 -> 73 steps
# random -> 80

# 5 candidates
#
# gamma = 0 -> 73 steps
# gamma = 0.5 -> 73 steps
# gamma = 1 -> 75 steps
# random -> 83

# 6 candidates

# 74 stps

