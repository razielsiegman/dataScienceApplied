#search

import state
import frontier

def search(n):
    s=state.create(n)
    #print(s)
    f=frontier.create(s)
    while not frontier.is_empty(f):
        s=frontier.remove(f)
        if state.is_target(s):
            return [s, f[1], f[4], f[5]]
        ns=state.get_next(s)
        #print(ns)
        for i in ns:
            frontier.insert(f,i)
    return 0

#Runs the n-puzzle 100 times, where the dimension of the puzzle is the parameter
#prints the total number of pushes and pops, as well as the average depth
#For a 3x3 puzzle, average depth, pushes, and pops are around 6, 1800 and 1000. respectively.
#While depth is pretty consistent, pushes and pops have a significant variance
def experiment(size):
    n = 100
    avg_depth = 0
    pushes = 0
    pops = 0
    for i in range(n):
        temp = search(size)
        avg_depth += temp[1]
        pushes += temp[2]
        pops += temp[3]
    avg_depth = avg_depth / n
    pushes = pushes / n
    pops = pops /n
    return[avg_depth, pushes, pops]

answer = experiment(3)
print(answer)