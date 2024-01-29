from grid import Grid
from solver import Solver
g = Grid(2, 3)
print(g)
print("caca")
# # print (g.is_sorted())
# g.swap((0,0),(1,0))
# print(g)
g.swap_seq([((0,0),(1,0)),((1,2),(1,1))])
# print(g)
# print("les coord sont")
# print(g.coordonne(2))
print(g)
g=Solver(g)
print("reee ")
# g.bonne_colonne(3)
print(g.get_solution_naive())
print("pipi")
print(g)
# print(g)
# print(g.bonne_colonne(3))
# print("bonne colonne")

# print(g)
# g.bonne_ligne(6)
# print("bonne ligne")

# print(g)
















#print(g.is_sorted())
data_path = "../input/"
file_name = data_path + "grid0.in"

print(file_name)

g = Grid.grid_from_file(file_name)
print(g) 
