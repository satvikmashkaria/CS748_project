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

def get_bounds(pairwise_CIs, args):
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
    return bounds

def winner(pairwise_CIs, args):
    bounds = get_bounds(pairwise_CIs, args)
    # print(bounds)
    for c in args['candidates']:
        is_winner = True
        for c2 in args['candidates']:
            if c2!=c and bounds[c+'l'] <= bounds[c2+'u']: is_winner = False
        if is_winner: return c
    return None


def random_heuristic(pairwise_CIs, args):
    combs = list(combinations(args['candidates'], 2))
    combs = list(filter(lambda x: args['already_decided'][x] != 1, combs))
    random.shuffle(combs)
    kpairs = combs[:args['ques_limit']]
    return kpairs


def greedy_winner_heuristic(pairwise_CIs, args):
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

def dcb_winner_heuristic(pairwise_CIs, args, idx):
    def calc_A_B():
        bounds = get_bounds(pairwise_CIs, args)
        LCB_A = max([bounds[c+'l'] for c in args['candidates']])
        A = random.choice([c for c in args['candidates'] if bounds[c+'l']==LCB_A])
        UCB_B = max([bounds[c+'u'] for c in args['candidates'] if c!=A])
        B = random.choice([c for c in args['candidates'] if bounds[c+'u']==UCB_B and c!=A])
        return A, B

    A, B = calc_A_B()
    if idx%2==0:
        selected = []
        for c in args['candidates']:
            if c!=A and pairwise_CIs[(A, c)][0] < args['N']/2 and pairwise_CIs[(A, c)][1] > args['N']/2:
                selected.append((pairwise_CIs[(A, c)][1] - pairwise_CIs[(c, A)][0], (A, c)))
        random.shuffle(selected)
        selected.sort(reverse=True, key=lambda x:x[0])
        # print(idx, 'A', selected)
        return [p[1] for p in selected[:args['ques_limit']]]
    else:
        selected = []
        for c in args['candidates']:
            if c!=B and pairwise_CIs[(B, c)][0] < args['N']/2 and pairwise_CIs[(B, c)][1] > args['N']/2:
                selected.append((pairwise_CIs[(c, B)][1] - pairwise_CIs[(B, c)][0], (B, c)))
        random.shuffle(selected)
        selected.sort(reverse=True, key=lambda x:x[0])
        # print(idx, 'B', selected)
        return [p[1] for p in selected[:args['ques_limit']]]


def mod_dcb_winner_heuristic(pairwise_CIs, args, idx):
    def calc_A_B():
        bounds = get_bounds(pairwise_CIs, args)
        LCB_A = max([bounds[c+'l'] for c in args['candidates']])
        A = random.choice([c for c in args['candidates'] if bounds[c+'l']==LCB_A])
        UCB_B = max([bounds[c+'u'] for c in args['candidates'] if c!=A])
        B = random.choice([c for c in args['candidates'] if bounds[c+'u']==UCB_B and c!=A])
        return A, B

    A, B = calc_A_B()
    def chose_by_A():
        selected = []
        for c in args['candidates']:
            if c!=A and pairwise_CIs[(A, c)][0] < args['N']/2 and pairwise_CIs[(A, c)][1] > args['N']/2:
                selected.append((pairwise_CIs[(A, c)][1] - pairwise_CIs[(c, A)][0], (A, c)))
        random.shuffle(selected)
        selected.sort(reverse=True, key=lambda x:x[0])
        # print(idx, 'A', selected)
        return [p[1] for p in selected[:args['ques_limit']]]
    def chose_by_B():
        selected = []
        for c in args['candidates']:
            if c!=B and pairwise_CIs[(B, c)][0] < args['N']/2 and pairwise_CIs[(B, c)][1] > args['N']/2:
                selected.append((pairwise_CIs[(c, B)][1] - pairwise_CIs[(B, c)][0], (B, c)))
        random.shuffle(selected)
        selected.sort(reverse=True, key=lambda x:x[0])
        # print(idx, 'B', selected)
        return [p[1] for p in selected[:args['ques_limit']]]
    def chose_all():
        combs = list(combinations(args['candidates'], 2))
        combs = list(filter(lambda x: args['already_decided'][x] != 1, combs))
        random.shuffle(combs)
        return combs
    def merge_lists(f, s, t):
        ans = []
        for ele in f:
            if sorted(ele) not in ans: ans.append(sorted(ele))
        for ele in s:
            if sorted(ele) not in ans: ans.append(sorted(ele))
        for ele in t:
            if sorted(ele) not in ans: ans.append(sorted(ele))
        return ans[:args['ques_limit']]
    if idx%2==0: return merge_lists(chose_by_A(), chose_by_B(), chose_all())
    else: return merge_lists(chose_by_B(), chose_by_A(), chose_all())


def sample_complexity(args):
    n_voters = args['n_voters']
    args['N'] = n_voters
    probs = args['probs']
    probs = [i / sum(probs) for i in probs]
    probs = sorted(probs, reverse=True)
    n_candidates = len(probs)
    # n_candidates = 16
    args['n_candidates'] = n_candidates
    np.random.seed(args['seed'])
    random.seed(args['seed'])

    data = np.array([np.random.choice(range(1, n_candidates + 1), size=n_candidates, replace=False, p=probs).astype(str) for i in range(n_voters)])
    # data = np.load('../US_data_clean.npy')
    # np.random.shuffle(data)

    alpha = args['alpha']
    BB_alpha = 1
    BB_beta = 1
    t = np.arange(1, args['N'] + 1)

    args['candidates'] = [str(i) for i in range(1, n_candidates + 1)]
    pairwise_wins = defaultdict(list)
    args['already_decided'] = defaultdict(list)
    pairwise_CIs = defaultdict(list)
    for a, b in combinations(args['candidates'], 2):
        pairwise_CIs[(a, b)] = [0, args['N']]
        pairwise_CIs[(b, a)] = [0, args['N']]

    for i in tqdm.tqdm(range(args['N'])):
    # for i in range(args['N']):
        # print("voter: ", i)
        if args['heuristic'] == 'random': next_set = random_heuristic(pairwise_CIs, args)
        elif args['heuristic'] == 'dcb': next_set = dcb_winner_heuristic(pairwise_CIs, args, i)
        elif args['heuristic'] == 'mod_dcb': next_set = mod_dcb_winner_heuristic(pairwise_CIs, args, i)
        else: next_set = greedy_winner_heuristic(pairwise_CIs, args)
        # if i%10==0: print(i, next_set)
        vote = list(data[i])
        for a, b in next_set:
            a, b = str(a), str(b)
            pairwise_wins[(a, b)].append(1 if vote.index(a) < vote.index(b) else 0)
            pairwise_wins[(b, a)].append(0 if vote.index(a) < vote.index(b) else 1)

        for p in pairwise_wins:
            output = cswor.BBHG_confseq(pairwise_wins[p], args['N'], BB_alpha, BB_beta, alpha=alpha, running_intersection=True)
            pairwise_CIs[p] = [output[0][-1], output[1][-1]]
            pairwise_CIs[(p[1], p[0])] = [args['N'] - output[1][-1], args['N'] - output[0][-1]]

        curr_winner = winner(pairwise_CIs, args)
        if curr_winner:
            return i+1, curr_winner
    return args['N'], None


if __name__ == "__main__":
    args = {}
    # args['heuristic'] = 'random'
    args['heuristic'] = 'greedy'
    # args['heuristic'] = 'dcb'
    # args['heuristic'] = 'mod_dcb'
    args['n_voters'] = 1000
    # args['n_voters'] = 4639
    args['alpha'] = 0.05
    # args['probs'] = [0.4, 0.45, 0.5, 0.7, 0.8]
    args['probs'] = [0.1 for i in range(10)]
    # args['seed'] = 42
    args['seed'] = 5
    args['ques_limit'] = 10
    # args['ques_limit'] = 2
    args['gamma'] = 0.5
    # args['']
    print("Algorithm: ", args['heuristic'])
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

# 74 stp