# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid
from solver import Solver

class Test_Grid3(unittest.TestCase):
    def test_grid3(self):
        gOriginal = Grid.grid_from_file("input/grid3.in")
        
        # display_grid_result = False
        # g = gOriginal.clone()

        # print("Naive :")
        # g=Solver(g)
        # result = g.get_solution_naive()        
        # Solver.display(result, display_grid_result)

        # #------------A * 
        # print("A* :")
        # g = gOriginal.clone()
        # g=Solver(g)
        # result = g.a_star()
        # Solver.display(result, display_grid_result)
        #----------

        print("BSF :")
        # g = gOriginal.clone()
        # g=Solver(gOriginal)
        # result = g.bfs2()
        # Solver.display(result, display_grid_result)

        print(hash(gOriginal))


if __name__ == '__main__':
    unittest.main()