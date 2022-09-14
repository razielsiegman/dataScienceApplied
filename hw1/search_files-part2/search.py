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
            return [s, f[1],f[2]]
        ns=state.get_next(s)
        for i in ns:
            frontier.insert(f,i)

#Runs the n-puzzle 100 times, where the dimension of the puzzle is the parameter
#prints the total number of pushes and pops, as well as the path length
#The following are the typical path length, push and pop values, respectively, for a 3x3 puzzle:
#hdistance: 6, 800, 500
#hdistance1: 6, 40, 25
#hdistance2: 6, 25, 15
#No discernable difference was noticed when using a weighted A* algorithm
def experiment(size):
    n = 1000
    pushes = 0
    pops = 0
    path_length = 0
    for i in range(n):
        temp = search(size)
        path_length += len(temp[0][1])
        pushes += temp[1]
        pops += temp[2]
    pushes = pushes / n
    pops = pops /n
    path_length = path_length / n
    return[path_length, pushes, pops]

answer = experiment(3)
print(answer)


