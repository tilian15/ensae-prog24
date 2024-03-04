import grid


def pbo_global_hashage(aGrid):
    print (aGrid)

    pre =  str(aGrid.m) + ";" +  str(aGrid.n) 
    for i in range(0,aGrid.m):
        for j in range(0,aGrid.n):
            pre = pre + ";" + str(aGrid.state[i][j])
    return pre
    
def pbo_get_grid_from_hash(hash):
    l = hash.split(';')
    m = int(l[0])
    n = int(l[1])
    index = 2
    state = []
    for i in range (0,m):
        line = []
        for j in range (0,n):
            line.append(int(l[index]))
            index = index + 1
        state.append(line)
    return Grid(m,n,state)


g = grid.Grid(8, 3)
print(g)
print(g.state)



hash = pbo_global_hashage(g) 
print("Hash : %s " % hash)

g = grid.pbo_get_grid_from_hash(hash)

print(g)
