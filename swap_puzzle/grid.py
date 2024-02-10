"""
This is the grid module. It contains the Grid class and its associated methods.
"""
from graph import Graph 
import random
import numpy as np 

def global_haschage(values):
        a=''
        for i in values : 
            for j in i : 
                a+=str(j)
        return(int(a))

# From a hash, create a Grid
def get_grid_from_hash(m,n,hash):
    i = 0
    tab = []
    line  = []
    for a in str(hash):
        line.append(int(a))
        i = i + 1
        if (i == n) :
            tab.append(line)
            i = 0
            line = []
    return Grid(m, n, tab)


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
        return f"<grid.Grid: m={self.m}, n={self.n}>"

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
        print(coordonne_a)
        print(bonne_ligne)
    
        while coordonne_a[0] > bonne_ligne:
            self.swap(coordonne_a, (coordonne_a[0] - 1, coordonne_a[1]))
            l.append(((coordonne_a[0] - 1, coordonne_a[1]),(coordonne_a[0],coordonne_a[1])))
            coordonne_a = self.coordonne(a)
           
        while coordonne_a[0] < bonne_ligne:
            self.swap(coordonne_a, (coordonne_a[0] + 1, coordonne_a[1]))
            l.append(((coordonne_a[0],coordonne_a[1]),(coordonne_a[0] + 1, coordonne_a[1])))
            coordonne_a = self.coordonne(a)
        return l
    

    # def haschage(self): #permet à chaque grille de renvoyer une serie de chiffre afin de l'identifier comme un int et pouvoir la faire correspondre à un noeud
    #     a=''
    #     for i in self.state : 
    #         for j in i : 
    #             a+=str(j)
    #     return(int(a))

    # def haschage(self): #permet à chaque grille de renvoyer une serie de chiffre afin de l'identifier comme un int et pouvoir la faire correspondre à un noeud
    #     return globalHaschage(self.state)
     
    def etat_possible(self):
        l=[]
        for j in range(len(self.state)):
            for i in range(len(self.state[0])-1):
                self.swap((j,i+1),(j,i))
                
                a = [row[:] for row in self.state]
                #print(a)
                l.append((((j,i+1),(j,i)),a))  #probleme (résolu), le a qui est ajouté a la liste n'est pas le meme que celui afficher au dessus, pb resolu grace a une copie de self.state
                self.swap((j,i+1),(j,i))
        for y in range(len(self.state[0])):
            for k in range(len(self.state)-1):
                self.swap((k+1,y),(k,y))
                a = [row[:] for row in self.state]
                l.append((((k+1,y),(k,y)),a))
                self.swap((k+1,y),(k,y))
        return l 
    
    def etat_possible_to_haschage(self):
        etat_poss=self.etat_possible()
        #print(etat_poss)
        a = [row[:] for row in etat_poss]
        for i in range(len(etat_poss)):
            
            a[i]=(etat_poss[i][0],global_haschage(etat_poss[i][1]))
            
        return a

    # def grid_to_graph(self):
    #     graph = {}

    #     def add_edge(node1, node2):
    #         if node1 not in graph:
    #             graph[node1] = []
    #         graph[node1].append(node2)

    #     def explore_state(current_state):
    #         print ('explorer state ')
    #         print (current_state)
    #         # current_hash = self.haschage()
    #         current_hash = current_state
    #         self.visited.append(current_hash)

    #         possible_states = self.etat_possible_to_haschage() #le pb est que self.etat_possible_to_haschage se réalise sur la toute premirere grille alors que je veux qu'elle se fasse sur la nouvelle grille issus de current_state

    #         for move, next_state_hash in possible_states:
    #             add_edge(current_hash, next_state_hash)

    #             if next_state_hash not in self.visited:
    #                 explore_state(next_state_hash)

    #     self.visited = []
    #     explore_state(self.haschage())

    #     # def explore_state(self):
    #     #     current_state=globalHaschage(self)
    #     #     print ('explorer state ')
    #     #     print (current_state)
    #     #     # current_hash = self.haschage()
    #     #     current_hash = current_state
    #     #     self.visited.append(current_hash)

    #     #     possible_states = self.etat_possible_to_haschage()

    #     #     for move, next_state_hash in possible_states:
    #     #         add_edge(current_hash, next_state_hash)

    #     #         if next_state_hash not in self.visited:
    #     #             explore_state(next_state_hash)

    #     # self.visited = []
    #     # explore_state(self)

    # #afficher comme l'affichage de graph1.in
    #     for node, neighbors in graph.items():
    #         for neighbor in neighbors:
    #             print(f"{node} {neighbor}")

    def grid_to_graph(self):
        graph = Graph()

        # def add_edge(node1, node2):
        #     if node1 not in graph:
        #         graph[node1] = []
        #     graph[node1].append(node2)

        def explore_state(gridHash):
            print ('explorer state ')
            print (gridHash)
            gridToManipulate = get_grid_from_hash(self.m, self.n, gridHash)
            # current_hash = self.haschage()
            current_hash = gridHash
            self.visited.append(gridHash)

            possible_states =  gridToManipulate.etat_possible_to_haschage()

            for move, next_state_hash in possible_states:
                print ("->" + str(next_state_hash))
                graph.add_edge(current_hash, next_state_hash)

                if next_state_hash not in self.visited:
                    explore_state(next_state_hash)

        self.visited = []
        explore_state(self.hashage())

    #afficher comme l'affichage de graph1.in
        # for node, neighbors in graph.items():
        #     for neighbor in neighbors:
        #         print(f"{node} {neighbor}")

        return graph


          

        

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


    def hashage(self):
        return global_haschage(self.state)
    
