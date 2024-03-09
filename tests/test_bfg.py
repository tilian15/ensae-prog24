import sys 
sys.path.append("swap_puzzle/")

import unittest 
import grid as gridLib
import graph as graphLib

import heapq


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


    def test_hash(self):
        g1 = gridLib.Grid(2,2)
        g2 = gridLib.Grid(2,2)
        self.assertEqual(g1,g2)

        l = []
        l.append(g1)
        self.assertEqual(g2 in l, True)




    def test_grid4(self):
         grid = gridLib.Grid(2,2)
         print(grid)
         grid.swap((0,0), (0,1))
         grid.swap((1,0), (1,1))
         print(grid)
         # #self.assertEqual(grid.state, [[1, 2], [3, 4], [5, 6], [7, 8]])

         graph=grid.grid_to_graph()
         print(graph)
         print ('Compute BFS:')
         result = graph.bfs2(grid,1234)
         print ('BFS:')
         print (result)
    def test_checkGraph1In(self):
        graph = graphLib.Graph.graph_from_file("./input/graph1.in")
        # print(graph)
        # print("*********")
        # print(graph.bfs2(1,2))
        # print("*********")
        # print(graph.bfs2(1,4))

        # Check 
        solution_file =  open("./input/graph1.path.out", 'r')

        for l in solution_file.readlines():
            a = l.split(' ')
            
            src = int(a[0])
            dst = int(a[1])
            result_expected = l[l.index('['):-1]
            
            result = graph.bfs2(src,dst)
            result_string = '[' + ', '.join(str (a) for a in result) + ']'
            
            
            self.assertEqual(result_string, result_expected)
            # if (result_string != result_expected) :
            #     print ('************')
            #     print(l)
            
        solution_file.close()


    def test_checkGraph2In(self):
        graph = graphLib.Graph.graph_from_file("./input/graph2.in")

        # Check 
        solution_file =  open("./input/graph2.path.out", 'r')

        for l in solution_file.readlines():
            a = l.split(' ')
            
            src = int(a[0])
            dst = int(a[1])
            if ('[' not in l):
                result_expected = 'None'
            else :
                result_expected = l[l.index('['):-1]
            
            result = graph.bfs2(src,dst)
            if (result != None):
                result_string = '[' + ', '.join(str (a) for a in result) + ']'
            else :
                result_string = 'None'
            
            self.assertEqual(result_string, result_expected)
            # if (result_string != result_expected) :
            #     print ('************')
            #     print(l)
            
        solution_file.close()
if __name__ == '__main__':
    unittest.main()
