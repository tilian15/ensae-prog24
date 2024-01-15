from grid import Grid

g = Grid(2, 3)
print(g)
print (g.is_sorted())
g.swap((0,0),(1,0))
print(g)
g.swap_seq([((0,0),(1,0)),((1,2),(1,1))])
print(g)

print(g.is_sorted())
data_path = "../input/"
file_name = data_path + "grid0.in"

print(file_name)

g = Grid.grid_from_file(file_name)
print(g) 
