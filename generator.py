import random
def _gen():
    base = 3
    side = base*base
    def pattern(i, j):
        return (base * (i % base)+i // base + j) % side
    def shuffle(k):
        return random.sample(k, len(k))
    rBase = range(base)
    rows = [g * base + i for g in shuffle(rBase) for i in shuffle(rBase)]
    cols = [g*base + j for g in shuffle(rBase) for j in shuffle(rBase)]
    nums = shuffle(range(1, base*base+1))
    board = [[nums[pattern(i, j)] for j in cols] for i in rows]
    return board
def _gen2():
    base = 2
    side = base * base
    def pattern(i, j):
        return (base * (i % base) + i // base + j) % side
    def shuffle(k):
        return random.sample(k, len(k))
    rBase = range(base)
    rows = [g * base + i for g in shuffle(rBase) for i in shuffle(rBase)]
    cols = [g * base + j for g in shuffle(rBase) for j in shuffle(rBase)]
    nums = shuffle(range(1, base * base + 1))
    board = [[nums[pattern(i, j)] for j in cols] for i in rows]
    return board