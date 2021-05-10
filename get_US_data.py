import pandas as pd
import csv
import numpy as np

csv_name = "US_elect_full_data.csv"
# read_file = pd.read_excel("US_elect_county.xls", sheet_name="FULL DATA")
# read_file.to_csv(csv_name)

reader = csv.reader(open(csv_name, "r"))

rows = list(reader)

columns = rows[0]
rows = rows[1:]

print("Number of candidates: ", len(rows))
# print("Columns: ", columns)

inds = []
for i, col in enumerate(columns):
    if 'Votes' in col:
        inds.append(i)

num_candidates = len(inds)
print("NUm candidates: ", num_candidates)
candidates = [str(i) for i in range(num_candidates)]

data = []

for row in rows:
    # votes = {}
    temp = None

    votes = np.random.rand(num_candidates)
    for candidate, i in zip(candidates, inds):
        # print("Order: ", int(float((row[i - 8]))))
        order = row[i-8]
        if order != '':
            order = int(float(order))
            votes[order - 1] = float(row[i])
        # if row[i] == '':
        #     temp = np.random.rand()
        # else:
        #     temp = row[i]

        # votes[candidate] = float(temp)
    # print(votes)
    votes = -votes
    votes = np.argsort(votes) + 1
    votes = votes.astype(str)
    # votes = sorted(votes.items(), key=lambda x: -x[1])
    # print(votes)
    # votes = [i[0] for i in votes]
    print(votes)
    data.append(votes)
    # if votes != candidates:
    #     print(votes)
    #
    # print(row)
    # print(len(row), row)
    # exit(0)

data = np.array(data)
print(data.shape)

np.save("US_data_clean", data)
