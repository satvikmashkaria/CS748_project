from collections import defaultdict
from itertools import permutations
from itertools import combinations
import sys
import numpy as np
# np.random.seed(int(sys.argv[1]))
sys.path.insert(1, './cswor')
import cswor
import tqdm
import random


def winner(pairwise_CIs, args):
    # global args['candidates'], args['already_decided']
    # pairwise_CIs = defaultdict(list) ##
    # args['candidates'] = list(map(str, list(range(4)))) ##
    bounds = {}
    for c in args['candidates']:
        wins, losses = 0, 0
        for c2 in args['candidates']:
            if (c, c2) in pairwise_CIs:
                if pairwise_CIs[(c, c2)][0] > args['N']/2:
                    wins += 1
                    args['already_decided'][(c, c2)] = 1
                if pairwise_CIs[(c, c2)][1] < args['N']/2:
                    losses += 1
                    args['already_decided'][(c, c2)] = 1
        ties = (args['n_candidates']-1) - wins - losses
        bounds[c+'l'] = wins-losses-ties
        bounds[c+'u'] = wins-losses+ties
    print("bounds", bounds)
    for c in args['candidates']:
        is_winner = True
        for c2 in args['candidates']:
            if c2!=c and bounds[c+'l'] <= bounds[c2+'u']: is_winner = False
        if is_winner: return c
    return None


def random_heuristic(pairwise_CIs, args):

    # global n_candidates, args['ques_limit'], args['candidates'], args['already_decided']
    combs = list(combinations(args['candidates'], 2))
    combs = list(filter(lambda x: args['already_decided'][x] != 1, combs))
    random.shuffle(combs)
    kpairs = combs[:args['ques_limit']]
    return kpairs


def greedy_winner_heuristic(pairwise_CIs, args, ind):

    # global n_candidates, args['ques_limit'], args['candidates'], args['already_decided'], N
    # n_candidates, args['ques_limit'], args['candidates'], args['already_decided'], N = args['n_candidates'], args['ques_limit'], args['args['candidates']'], args['args['already_decided']'], N
    scores = defaultdict(list)

    for (a, b) in pairwise_CIs:
        [lb, ub] = pairwise_CIs[(a, b)]
        scores[(a, b)] = (abs(ub - args['N']/2) - abs(args['N']/2 - lb))/(ub - lb + 1e-4)

    winning_probs = {}

    for c in args['candidates']:
        wp = 0
        for c1 in args['candidates']:
            if (c, c1) in scores:
                wp += scores[(c, c1)]
        winning_probs[c] = wp

    impact = defaultdict(float)

    for (a, b) in pairwise_CIs:
        impact[(a, b)] = winning_probs[a] + winning_probs[b]

    gamma = args['gamma']
    for (a, b) in scores:
        scores[(a, b)] = gamma * abs(scores[(a, b)]) + (1 - gamma) * impact[(a, b)] / (2 * (args['n_candidates'] - 1))
    scores = sorted(scores.items(), key = lambda kv: -kv[1])
    selected = [i[0] for i in scores][0::2]
    selected = list(filter(lambda x: args['already_decided'][x] != 1, selected))
    selected = selected[:args['ques_limit']]

    return selected


def dcb_heuristic(pairwise_CIs, args, ind):

    if ind % 2 == 0:
        score = defaultdict(list)
        for (a, b) in pairwise_CIs:
            [lb_a, ub_a] = pairwise_CIs[(a, b)]
            [lb_b, ub_b] = pairwise_CIs[(b, a)]
            # scores[(a, b)] = (abs(ub - args['N'] / 2) - abs(args['N'] / 2 - lb)) / (ub - lb + 1e-4)
    else:
        scores = defaultdict(list)
        for (a, b) in pairwise_CIs:
            [lb, ub] = pairwise_CIs[(a, b)]
            scores[(a, b)] = (abs(ub - args['N'] / 2) - abs(args['N'] / 2 - lb)) / (ub - lb + 1e-4)




def sample_complexity(args):
    n_voters = args['n_voters']
    args['N'] = n_voters
    probs = args['probs']
    probs = [i / sum(probs) for i in probs]
    probs = sorted(probs, reverse=True)
    # n_candidates = len(probs)
    n_candidates = 16
    args['n_candidates'] = n_candidates
    np.random.seed(args['seed'])
    random.seed(args['seed'])

    # data = np.array([np.random.choice(range(1, n_candidates + 1), size=n_candidates, replace=False, p=probs).astype(str) for i in range(n_voters)])
    data = np.load("../US_data_clean.npy")
    np.random.shuffle(data)
    # print(data[:20])
    # print(data.shape)
    alpha = args['alpha']
    BB_alpha = 1
    BB_beta = 1
    t = np.arange(1, args['N'] + 1)

    args['candidates'] = [str(i) for i in range(1, n_candidates + 1)]
    pairwise_wins = defaultdict(list)
    args['already_decided'] = defaultdict(int)
    pairwise_CIs = defaultdict(list)

    for a, b in combinations(args['candidates'], 2):
        pairwise_CIs[(a, b)] = [0, args['N']]
        pairwise_CIs[(b, a)] = [0, args['N']]

    for i in tqdm.tqdm(range(args['N'])):
        # print("voter: ", i)
        if args['heuristic'] == 'random': next_set = random_heuristic(pairwise_CIs, args)
        elif args['heuristic'] == 'greedy': next_set = greedy_winner_heuristic(pairwise_CIs, args, i)
        else: next_set = dcb_heuristic(pairwise_CIs, args, i)
        print(i, next_set)
        vote = list(data[i])
        # print("Al decided: ", args['already_decided'])
        print("12222", pairwise_CIs[('1', '2')])
        for a, b in next_set:
            a, b = str(a), str(b)
            pairwise_wins[(a, b)].append(1 if vote.index(a) < vote.index(b) else 0)
            pairwise_wins[(b, a)].append(0 if vote.index(a) < vote.index(b) else 1)

        # for a, b in combinations(args['candidates'], 2):
        #     pairwise_CIs[(a, b)] = [0, args['N']]
        #     pairwise_CIs[(b, a)] = [0, args['N']]

        for p in pairwise_wins:
            output = cswor.BBHG_confseq(pairwise_wins[p], args['N'], BB_alpha, BB_beta, alpha=alpha, running_intersection=True)
            pairwise_CIs[p] = [output[0][-1], output[1][-1]]
            pairwise_CIs[(p[1], p[0])] = [args['N'] - output[1][-1], args['N'] - output[0][-1]]

        curr_winner = winner(pairwise_CIs, args)
        if curr_winner:
            return i+1, curr_winner


if __name__ == "__main__":
    args = {}
    # args['heuristic'] = 'random'
    args['heuristic'] = 'greedy'
    # args['heuristic'] = 'dcb'
    args['n_voters'] = 4639
    args['alpha'] = 0.05
    args['probs'] = [0.4, 0.45, 0.5, 0.7, 0.8]
    args['seed'] = 51
    args['ques_limit'] = 5
    args['gamma'] = 0.5
    print(sample_complexity(args))



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


# Yateesh function
# def sample_complexity(args):
#     n_voters = args['n_voters']
#     args['N'] = n_voters
#     probs = args['probs']
#     probs = [i / sum(probs) for i in probs]
#     probs = sorted(probs, reverse=True)
#     # n_candidates = len(probs)
#     n_candidates = 16
#     args['n_candidates'] = n_candidates
#     np.random.seed(args['seed'])
#     random.seed(args['seed'])
#
#     # data = np.array([np.random.choice(range(1, n_candidates + 1), size=n_candidates, replace=False, p=probs).astype(str) for i in range(n_voters)])
#     data = np.load('../US_data_clean.npy')
#     random.shuffle(data)
#
#     alpha = args['alpha']
#     BB_alpha = 1
#     BB_beta = 1
#     t = np.arange(1, args['N'] + 1)
#
#     args['candidates'] = [str(i) for i in range(1, n_candidates + 1)]
#     pairwise_wins = defaultdict(list)
#     args['already_decided'] = defaultdict(list)
#     pairwise_CIs = defaultdict(list)
#     for a, b in combinations(args['candidates'], 2):
#         pairwise_CIs[(a, b)] = [0, args['N']]
#         pairwise_CIs[(b, a)] = [0, args['N']]
#
#     for i in tqdm.tqdm(range(args['N'])):
#     # for i in range(args['N']):
#         # print("voter: ", i)
#         if args['heuristic'] == 'random': next_set = random_heuristic(pairwise_CIs, args)
#         elif args['heuristic'] == 'dcb': next_set = dcb_winner_heuristic(pairwise_CIs, args, i)
#         elif args['heuristic'] == 'mod_dcb': next_set = mod_dcb_winner_heuristic(pairwise_CIs, args, i)
#         else: next_set = greedy_winner_heuristic(pairwise_CIs, args, i)
#         # if i%10==0: print(i, next_set)
#         vote = list(data[i])
#         for a, b in next_set:
#             a, b = str(a), str(b)
#             pairwise_wins[(a, b)].append(1 if vote.index(a) < vote.index(b) else 0)
#             pairwise_wins[(b, a)].append(0 if vote.index(a) < vote.index(b) else 1)
#
#         for p in pairwise_wins:
#             output = cswor.BBHG_confseq(pairwise_wins[p], args['N'], BB_alpha, BB_beta, alpha=alpha, running_intersection=True)
#             pairwise_CIs[p] = [output[0][-1], output[1][-1]]
#             pairwise_CIs[(p[1], p[0])] = [args['N'] - output[1][-1], args['N'] - output[0][-1]]
#
#         curr_winner = winner(pairwise_CIs, args)
#         if curr_winner:
#             return i+1, curr_winner
#     return args['N'], None

