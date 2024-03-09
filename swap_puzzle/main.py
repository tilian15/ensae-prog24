from grid import Grid
# from grid import global_haschage2
# from grid import get_grid_from_hashfinal


####
# Exemple interessant
# [7, 5, 3]
# [2, 8, 6]
# [4, 1, 9]
# Solution Naive :
# (0.0, 7, [<grid.Grid: m=3, n=3, state=[[7, 5, 3], [2, 8, 6], [4, 1, 9]]>, <grid.Grid: m=3, n=3, state=[[7, 5, 3], [2, 8, 6], [1, 4, 9]]>, <grid.Grid: m=3, n=3, state=[[7, 5, 3], [1, 8, 6], [2, 4, 9]]>, <grid.Grid: m=3, n=3, state=[[1, 5, 3], [7, 8, 6], [2, 4, 9]]>, <grid.Grid: m=3, n=3, state=[[1, 5, 3], [7, 8, 6], [4, 2, 9]]>, <grid.Grid: m=3, n=3, state=[[1, 5, 3], [7, 2, 6], [4, 8, 9]]>, <grid.Grid: m=3, 
# n=3, state=[[1, 2, 3], [7, 5, 6], [4, 8, 9]]>, <grid.Grid: m=3, n=3, state=[[1, 2, 3], [4, 5, 6], [7, 8, 9]]>])
# Nb of swap : 7
# Time : 0.0
# A* :
# chemin issu de A*
# Nb of swap : 5
# Time : 0.003987312316894531
# BSF :
# Nb of swap : 5
# Time : 354.874897480011



from solver import Solver
from ui import SwapGenerator
g = Grid(3, 3)




nb_row = 3
nb_column = 3
nb_swaps = 10
display_grid_result = False

gOriginal = Grid(nb_row, nb_column)
swap_generator = SwapGenerator()
swaps = swap_generator.generate_swaps(nb_swaps, nb_row, nb_column)
print(swaps)



gOriginal.swap_seq(swaps)
print(gOriginal)

#gOriginal = Grid(nb_row, nb_column, [[7, 5, 3],[2, 8, 6],[4, 1, 9]])
#gOriginal = Grid(nb_row, nb_column, [[4,2],[3,1],[5,6]])


print("Solution Naive :")
g = gOriginal.clone()

g=Solver(g)
result = g.get_solution_naive()
print(result)
Solver.display(result, display_grid_result)

#------------A * 
print("A* :")
g = gOriginal.clone()
g=Solver(g)
result = g.a_star()
Solver.display(result, display_grid_result)
# #----------

#------------A * 
print("A* ancienne heuristique :")
g = gOriginal.clone()
g=Solver(g)
result = g.a_star_ancienne_heuristique()
Solver.display(result, display_grid_result)


print("BSF Optimize:")
g = gOriginal.clone()
g=Solver(g)
result = g.bfs2_optimise()
Solver.display(result, False)

print("BSF:")
g = gOriginal.clone()
g=Solver(g)
result = g.bfs2()
Solver.display(result, False)




