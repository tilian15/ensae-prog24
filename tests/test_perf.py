# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid
import time

class Test_Swap(unittest.TestCase):
    def test_perf(self):
        g = Grid(3,3)

        listOfGrid = g.grid_possible()

        listOfState = [a.state for a in listOfGrid]
        start_time = time.time()
        for i in range (0,10000):
            if (g.state in listOfState):
                a = 1
        print(time.time() - start_time)
        

        start_time = time.time()
        for i in range (0,10000):
            if (g in listOfGrid):
                a = 1
        print(time.time() - start_time)

        
        
        

    

if __name__ == '__main__':
    unittest.main()
