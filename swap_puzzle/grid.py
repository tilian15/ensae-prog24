"""
This is the grid module. It contains the Grid class and its associated methods.
"""
import graph as graphLib
import random
import numpy as np 

import time



class Grid():
    """
    A class representing the grid from the swap puzzle. It supports rectangular grids. 

    Attributes: 
    -----------
    m: int
        Number of lines in the grid
    n: int
        Number of columns in the grid
    state: list[list[int]]
        The state of the grid, a list of list such that state[i][j] is the number in the cell (i, j), i.e., in the i-th line and j-th column. 
        Note: lines are numbered 0..m and columns are numbered 0..n.
    """
    
    def __init__(self, m, n, initial_state = []):
        """
        Initializes the grid.

        Parameters: 
        -----------
        m: int
            Number of lines in the grid
        n: int
            Number of columns in the grid
        initial_state: list[list[int]]
            The intiail state of the grid. Default is empty (then the grid is created sorted).
        """
        self.m = m
        self.n = n
        if not initial_state:
            initial_state = [list(range(i*n+1, (i+1)*n+1)) for i in range(m)]            
        self.state = initial_state

    def __str__(self): 
        """
        Prints the state of the grid as text.
        """
        output = f"The grid is in the following state:\n"
        for i in range(self.m): 
            output += f"{self.state[i]}\n"
        return output

    def __repr__(self): 
        """
        Returns a representation of the grid with number of rows and columns.
        """
        return f"<grid.Grid: m={self.m}, n={self.n}, state={self.state}>"

    def is_sorted(self): #permet de verifier si la grille est bien triée
        """
        Checks is the current state of the grid is sorte and returns the answer as a boolean.
        """
        test = np.arange(1,(self.n * self.m )+1)
        #print(test)
        test2 = []
        for i in self.state:
            test2+=i
        #print(test2)
        return not(False in (test2 == test))


    # https://docs.python.org/3.5/reference/datamodel.html#object.__hash__
    # https://stackoverflow.com/questions/2909106/whats-a-correct-and-good-way-to-implement-hash
    # https://ioflood.com/blog/python-hash/
    # https://stackoverflow.com/questions/7027199/hashing-arrays-in-python
    def __key(self):
        # need to convert self.state to an str as array is not hashable / immutable        
        return (self.m, self.n, str(self.state))

    def __hash__(self):        
        return hash(self.__key())

    def __eq__(self, other):        
        if isinstance(other, Grid):
            return self.__key() == other.__key()
        return NotImplemented

    def __contains__(self,item):
        print ('contains')
        return True

    # To fix :
    # heapq.heappush(frontier, (priority, next_node))
    # TypeError: '<' not supported between instances of 'Grid' and 'Grid'
    def __lt__(self, other):
         if isinstance(other, Grid):
             return hash(self.__key()) == hash(other.__key())
         return NotImplemented
        
        

    def swap(self, cell1, cell2):
        """
        Implements the swap operation between two cells. Raises an exception if the swap is not allowed.

        Parameters: 
        -----------
        cell1, cell2: tuple[int]
            The two cells to swap. They must be in the format (i, j) where i is the line and j the column number of the cell. 
        """
        if (cell1[0] == cell2[0] and abs(cell1[1]-cell2[1]) == 1) or (cell1[1] == cell2[1] and abs(cell1[0]-cell2[0]) == 1): #verifie si la distance est bien égale à 1 et que les 2 cases sont cote à cote
            self.state[cell1[0]][cell1[1]], self.state[cell2[0]][cell2[1]] = self.state[cell2[0]][cell2[1]], self.state[cell1[0]][cell1[1]]
        else:
            print("error unavailable swap")
            print(cell1,cell2)


    def swap_seq(self, cell_pair_list):
        """
        Executes a sequence of swaps. 

        Parameters: 
        -----------
        cell_pair_list: list[tuple[tuple[int]]]
            List of swaps, each swap being a tuple of two cells (each cell being a tuple of integers). 
            So the format should be [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...].
        """ 
        for i in cell_pair_list:
            self.swap(i[0],i[1])


    
    def coordonne(self,a): #permet de renvoyer les coordonnées d'un chiffre dans la grille 
        for i in range(len(self.state)):
            for j in range(len(self.state[0])):
                if self.state[i][j]==a : 
                    return (i,j)
                

    def bonne_colonne(self,a): #permet de mettre un nombre sur sa bonne colonne 
        coordonne_a=self.coordonne(a)
        if a %self.n==0 : 
            bonne_colonne = self.n -1
        else : 
            bonne_colonne= a%self.n -1
        l=[]
        while coordonne_a[1]>bonne_colonne:
            self.swap(coordonne_a,((coordonne_a[0],coordonne_a[1]-1)))
            l.append(((coordonne_a[0],coordonne_a[1]),(coordonne_a[0],coordonne_a[1]-1)))
            coordonne_a=self.coordonne(a)
        while coordonne_a[1]<bonne_colonne:
            self.swap(coordonne_a,((coordonne_a[0],coordonne_a[1]+1)))
            l.append(((coordonne_a[0],coordonne_a[1]),(coordonne_a[0],coordonne_a[1]+1)))
            coordonne_a=self.coordonne(a)
        return l 


    def bonne_ligne(self, a):
    # permet de mettre un nombre sur sa bonne ligne
        coordonne_a = self.coordonne(a)
        if a%self.n == 0 :
            bonne_ligne = a//(self.n+1) 
        else :
            bonne_ligne = a //self.n 
        l = []
    
        while coordonne_a[0] > bonne_ligne:
            self.swap(coordonne_a, (coordonne_a[0] - 1, coordonne_a[1]))
            l.append(((coordonne_a[0] - 1, coordonne_a[1]),(coordonne_a[0],coordonne_a[1])))
            coordonne_a = self.coordonne(a)
           
        while coordonne_a[0] < bonne_ligne:
            self.swap(coordonne_a, (coordonne_a[0] + 1, coordonne_a[1]))
            l.append(((coordonne_a[0],coordonne_a[1]),(coordonne_a[0] + 1, coordonne_a[1])))
            coordonne_a = self.coordonne(a)
        return l
    

     
    # Return an array of  tuple ( move, newGrid) 
    def grid_possible(self):
        # start_time = time.time()
        l=[]
        for j in range(len(self.state)):
            for i in range(len(self.state[0])-1):
                a = self.clone()
                a.swap((j,i+1),(j,i))
                l.append(a)
                
        for y in range(len(self.state[0])):
            for k in range(len(self.state)-1):
                a = self.clone()
                a.swap((k+1,y),(k,y))
                l.append(a)
        # print(time.time() - start_time)
        return l 
    

    def clone(self):
        a = []
        for i in self.state:
            b = []
            for j in i:
                b.append(j)
            a.append(b)

        return Grid(self.m, self.n, a)
        
    


    def grid_to_graph(self):
        graph = graphLib.Graph()

        # def add_edge(node1, node2):
        #     if node1 not in graph:
        #         graph[node1] = []
        #     graph[node1].append(node2)

        def explore_state(grid):
            gridToManipulate = grid #get_grid_from_hash(self.m, self.n, gridHash)
            # current_hash = self.haschage()
            current_grid = grid
            self.visited.append(grid)

            possible_states =  gridToManipulate.grid_possible()

            

            for next_grid in possible_states:
                print ("->" + str(next_grid))
                print ('-------------***')
                print (current_grid)
                print ('-------------***')
                print (next_grid)
                print ('-------------***')
                graph.add_edge(current_grid, next_grid)

                if next_grid not in self.visited:
                    explore_state(next_grid)

        self.visited = []
        explore_state(self)
        return graph
    
    






    
    def heuristique(self):
        cpt=0
        indice=0
        for i in range(self.m):
            for j in range(self.n):
                indice+=1
                if self.state[i][j]!=indice : 
                    cpt+=1
        return cpt

    def heuristique2(self):
        cpt=0
        for i in range(self.m):
            for j in range(self.n):
                a=self.state[i][j]
                if a%self.n == 0 :
                    bonne_ligne = a//(self.n+1) 
                else :
                    bonne_ligne = a //self.n
                cpt+=abs(bonne_ligne - i)
                if a %self.n==0 : 
                    bonne_colonne = self.n -1
                else : 
                    bonne_colonne= a%self.n -1
                cpt+=abs( j - bonne_colonne)
        
        return cpt/2 #on divise par 2 car on compte les mouvements 2 fois comme à chaque fois on 'inverse' 2 cases 


    def heuristique3(self):
        #self=global_haschage2bis(a)
        cpt=0
        m = self.m #nbre de ligne
        n = self.n #nbre de colonne
        for i in range(m):
            for j in range(n):
                a=self.state[i][j]
                if a%n == 0 :
                    bonne_ligne = a//(n+1) 
                else :
                    bonne_ligne = a //n
                cpt+=abs(bonne_ligne - i)
                if a %n==0 : 
                    bonne_colonne = n -1
                else : 
                    bonne_colonne= a%n -1
                cpt+=abs( j - bonne_colonne)
        
        return cpt/2     

        

    @classmethod
    def grid_from_file(cls, file_name): 
        """
        Creates a grid object from class Grid, initialized with the information from the file file_name.
        
        Parameters: 
        -----------
        file_name: str
            Name of the file to load. The file must be of the format: 
            - first line contains "m n" 
            - next m lines contain n integers that represent the state of the corresponding cell

        Output: 
        -------
        grid: Grid
            The grid
        """
        with open(file_name, "r") as file:
            m, n = map(int, file.readline().split())
            initial_state = [[] for i_line in range(m)]
            for i_line in range(m):
                line_state = list(map(int, file.readline().split()))
                if len(line_state) != n: 
                    raise Exception("Format incorrect")
                initial_state[i_line] = line_state
            grid = Grid(m, n, initial_state)
        return grid


    
