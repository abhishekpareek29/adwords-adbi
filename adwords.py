import csv
import pandas as pd
import numpy as np
import random
import sys

# Set a seed.
random.seed(0)

# Implements Greedy algorithm
def Greedy(budgets, bids, queries):
  revenue = 0
  for q in queries:
    keys = bids[q].keys()
    keys = list(keys)
    highestBidder = keys[0]
    highestBid = -1

    c = check_budget(bids[q], budgets)
    if c != -1:
      for k in keys:
        if budgets[k] >= bids[q][k]:
          if highestBid < bids[q][k]:
            highestBidder = k
            highestBid = bids[q][k]
          elif highestBid == bids[q][k]:
            if highestBidder > k:
              highestBidder = k
              highestBid = bids[q][k]

      revenue += bids[q][highestBidder]
      budgets[highestBidder] -= bids[q][highestBidder]

    return revenue

# Implements Balance algorithm
def Balance(budget, bids, queries):
  revenue = 0
  for q in queries:
    b = bids[q]
    keys = b.keys()
    keys = list(keys)
    maxBidder = keys[0]
    c = check_budget(b, budget)
    if c == -1:
      return -1
    for k in keys:
      if budget[k] >= b[k]:
        if budget[maxBidder] < budget[k]:
          maxBidder = k
        elif budget[maxBidder] == budget[k]:
          if maxBidder > k:
            maxBidder = k

    bidder = maxBidder
    if bidder != -1:
      revenue += bids[q][bidder]
      budget[bidder] -= bids[q][bidder]

  return revenue

# Implements MSVV algorithm
def MSVV(rembudget, budgets, bids, queries):
  revenue = 0
  for q in queries:
    b = bids[q]
    keys = b.keys()
    keys = list(keys)
    maxBidder = keys[0]
    c = check_budget(b, rembudget)
    if c == -1:
      return -1
    for k in keys:
      if budgets[k] >= b[k]:
        m1 = scaledBid(b[maxBidder], rembudget[maxBidder], budgets[maxBidder])
        m2 = scaledBid(b[k], rembudget[k], budgets[k])
        if m1 < m2:
          maxBidder = k
        elif m1 == m2:
          if maxBidder > k:
            maxBidder = k
    bidder = maxBidder

    if bidder != -1:
      revenue += bids[q][bidder]
      rembudget[bidder] -= bids[q][bidder]

  return revenue

# Check if all bidders of a query have exhausted their budget.
def check_budget(b, budgets):
  keys = b.keys()
  for k in keys:
    if budgets[k] >= b[k]:
      return 0
  return -1

def psi (xu):
  return 1 - np.exp(xu-1)

# Scales the bid based on the remaining budget as per the MSVV algorithm
def scaledBid (bid, rembud, bud):
  xu = (bud-rembud)/bud
  return bid*psi(xu)

# Reports the average revenue
def calculate_revenue(budget, bids, queries, type):
  total_revenue = 0
  iters = 100
  for i in range(0,iters):
    random.shuffle(queries)
    budget1 = dict(budget)
    if type ==1:
      revenue = Greedy(budget1, bids, queries)
    elif type == 2:
      revenue = Balance(budget1, bids, queries)
    elif type == 3:
      revenue = MSVV(budget1, dict(budget), bids, queries)
    else:
      revenue = 0
    total_revenue += revenue

  return total_revenue/iters


# Main function.
def main(type):
  budget = dict()
  bids = dict()

  input = pd.read_csv('bidder_dataset.csv')

  for i in range(0, len(input)):
    a = input.iloc[i]['Advertiser']
    k = input.iloc[i]['Keyword']
    bv = input.iloc[i]['Bid Value']
    b = input.iloc[i]['Budget']
    if not (a in budget):
      budget[a] = b
    if not (k in bids):
      bids[k] = {}
    if not (a in bids[k]):
      bids[k][a] = bv

  with open('queries.txt') as f:
    queries = f.readlines()
  queries = [x.strip() for x in queries]

  r = calculate_revenue(budget, bids, queries, type)
  print(r)
  print (r/sum(budget.values()))

# Checks runtime arguemnts and accordingly run algorithms.
if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Invalid Input")
  else:
    if sys.argv[1] == 'greedy':
      main(1)
    elif sys.argv[1] == 'balance':
      main(2)
    elif sys.argv[1] == 'msvv':
      main(3)
    else:
      print('Invalid Input')
