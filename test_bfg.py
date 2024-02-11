import sys 
sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid

class Test_Swap(unittest.TestCase):


    # def test_grid1(self):
    #     grid = Grid(2,2)
    #     print(grid)
    #     grid.swap((0,0), (0,1))
    #     print(grid)
    #     #self.assertEqual(grid.state, [[1, 2], [3, 4], [5, 6], [7, 8]])

    #     graph=grid.grid_to_graph()
    #     print(graph)

    #     print ('Compute BFS:')
    #     result = graph.bfs(grid.hashage(),1234)
    #     print ('BFS:')
    #     print (result)

    


    # def test_grid2(self):
    #     grid = Grid(1,2)
    #     print(grid)
    #     grid.swap((0,0), (0,1))
    #     print(grid)
    #     # #self.assertEqual(grid.state, [[1, 2], [3, 4], [5, 6], [7, 8]])

    #     graph=grid.grid_to_graph()
    #     print(graph)
    #     print ('Compute BFS:')
    #     result = graph.bfs(grid.hashage(),12)
    #     print ('BFS:')
    #     print (result)

    # def test_grid3(self):
    #     grid = Grid(1,3)
    #     print(grid)
    #     grid.swap((0,0), (0,1))
    #     grid.swap((0,1), (0,2))
    #     print(grid)
    #     # #self.assertEqual(grid.state, [[1, 2], [3, 4], [5, 6], [7, 8]])

    #     graph=grid.grid_to_graph()
    #     print(graph)
    #     print ('Compute BFS:')
    #     result = graph.bfs(grid.hashage(),123)
    #     print ('BFS:')
    #     print (result)



    def test_grid4(self):
         grid = Grid(2,2)
         print(grid)
         grid.swap((0,0), (0,1))
         grid.swap((1,0), (1,1))
         print(grid)
         # #self.assertEqual(grid.state, [[1, 2], [3, 4], [5, 6], [7, 8]])

         graph=grid.grid_to_graph()
         print(graph)
         print ('Compute BFS:')
         result = graph.bfs2(grid.hashage(),1234)
         print ('BFS:')
         print (result)

if __name__ == '__main__':
    unittest.main()
