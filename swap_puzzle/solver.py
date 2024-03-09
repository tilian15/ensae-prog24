from grid import Grid
import matplotlib.pyplot as plt
from matplotlib.table import Table
import heapq
import time

# Function to centralize severals solvers
# Each function will return following tuple
# ( nb of move, time, array of grid)

def swap(self, cell1, cell2):
        """
        Implements the swap operation between two cells. Raises an exception if the swap is not allowed.

        Parameters: 
        -----------
        cell1, cell2: tuple[int]
            The two cells to swap. They must be in the format (i, j) where i is the line and j the column number of the cell. 
        """
        if (cell1[0] == cell2[0] and abs(cell1[1]-cell2[1]) == 1) or (cell1[1] == cell2[1] and abs(cell1[0]-cell2[0]) == 1): #verifie si la distance est bien égale à 1 et que les 2 cases sont cote à cote
            self[cell1[0]][cell1[1]], self[cell2[0]][cell2[1]] = self[cell2[0]][cell2[1]], self[cell1[0]][cell1[1]]
        else:
            print("error unavailable swap")
            print(cell1,cell2)
        return self

def etat_possible2(self):
        l=[]
        a = [row[:] for row in self]
        for j in range(len(self)):
            for i in range(len(self[0])-1):
                b = [row[:] for row in a]
                b= swap(b,(j,i+1),(j,i))
                l.append(b) 
        for y in range(len(self[0])):
            for k in range(len(self)-1):
                b = [row[:] for row in a]
                b=swap(b,(k+1,y),(k,y))
                l.append(b)

        return l

def global_haschage2bis(tab): #haschage à partir d'un tablo
    n=len(tab[0])
    m=len(tab)
    pre = str(m) + ';' + str(n)
    for i in range(0,m):
        for j in range(0,n):
            pre = pre + ";" + str(tab[i][j])
    return pre


class Solver(): 
    """
    A solver class, to be implemented.
    """

    def __init__(self,grid):
        self.grid = grid
    

    
    def get_solution_naive(self): #on va tenter de placer un par un les chiffres, de 1 à n*m en les placant dabord à leur colonne puis en les faisant monter 
        """
        Solves the grid and returns the sequence of swaps at the format 
        [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...]. 
        """
        start_time = time.time()
        clone = self.grid.clone()

        sequence = []
        for i in range(1,(self.grid.n * self.grid.m) +1 ):
            sequence2=[]
            sequence2+=self.grid.bonne_colonne(i)
            sequence2+=self.grid.bonne_ligne(i)
            sequence+=sequence2
        
        result = [clone.clone()]
        for a in sequence:

             clone.swap_seq([a])
             result.append(clone.clone())
            
        return (time.time() - start_time, len(result) - 1, result)

        

    def bfs2(self): #Question 8, ce bfs ne fonctionnera que pour swap_puzzle
        start_time = time.time()
        dst = Grid(self.grid.m,self.grid.n)            
        grids_done = []
        grids_todo = [self.grid]
        predecessors = {}
        predecessors = {self.grid: 0}
        #if we found the dst
        found = False
        if (dst == self.grid):
            found = True
        while len(grids_todo)>0 and not found :
            grid_to_analyse = grids_todo.pop(0)
            
            
            for n in grid_to_analyse.grid_possible(): 
                if n not in grids_done:
                    if (n not in grids_todo) :
                        grids_todo.append(n)
                        predecessors[n] = grid_to_analyse
                    #to exit the while
                    if (n == dst):
                        found = True

            grids_done.append(grid_to_analyse)
        if not found:
            return None 
                   
        
            
        result = []            
        previous = dst
        while (predecessors[previous] != 0):
            result.append(previous)
            previous = predecessors[previous]
        result.append(previous)
        result.reverse()
        return (time.time() - start_time, len(result) -1 , result)
    


    def bfs2_optimise(self): #Question 8, ce bfs ne fonctionnera que pour swap_puzzle 
        start_time = time.time()
        dst = Grid(self.grid.m,self.grid.n)    
        print("From "  + str(self.grid.state) + ' to ' + str(dst.state))
        nodes_done = []
        nodes_todo = [self.grid.state]
        predecessors = {}
        predecessors = {global_haschage2bis(self.grid.state): 0}
        #if we found the dst
        found = False
        if (dst == self.grid):
            found = True           
        while len(nodes_todo)>0 and not found :  #executer au maximum S fois avec S le nombre de noeuds           
            node_to_analyse = nodes_todo.pop(0) 
            for n in etat_possible2(node_to_analyse): # chaque noeud u a d(u) voisins, donc au max S-1, or chaque arrete est considérée au plus deux fois donc l'affectation est executée au maximum 2G fois avec G le nombre d'arretes.
                if n not in nodes_done:
                    if (n not in nodes_todo) :
                        nodes_todo.append(n) 
                        predecessors[global_haschage2bis(n)] = node_to_analyse 
                    #to exit the while
                    if (n == dst.state):
                        found = True

            nodes_done.append(node_to_analyse) #réalisé au plus S fois 
        if not found:
            return None 

            
            
        result = []            
        previous = dst.state
        while (predecessors[global_haschage2bis(previous)] != 0):
            result.append(Grid(self.grid.m, self.grid.n,previous))
            previous = predecessors[global_haschage2bis(previous)]
        result.append(Grid(self.grid.m, self.grid.n,previous))
        result.reverse()
        return (time.time() - start_time, len(result) -1 , result)
    # complexité : O(2G + S) + 0(1) * i (toutes les opérations constantes) = O(S + G)

    def a_star(self): #ne fonctionnera uniquement pour swap_puzzle
        start_time = time.time()
        goal = Grid(self.grid.m,self.grid.n) 
        frontier = []
        heapq.heappush(frontier, (0, self.grid))  # (priority, node)
        came_from = {}
        cost_so_far = {}
        came_from[self.grid] = None
        cost_so_far[self.grid] = 0
        while len(frontier) > 0 :
            current_cost, current_node = heapq.heappop(frontier)
            if current_node == goal:
                break
            for next_node in current_node.grid_possible(): # Accéder à la liste des voisins du nœud actuel dans le graphe
                new_cost = cost_so_far[current_node] + 1  # On suppose que le coût de chaque mouvement est 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + next_node.heuristique3()                    
                    heapq.heappush(frontier, (priority, next_node))
                    came_from[next_node] = current_node
        path = []
        node = goal
        while node != self.grid:
            path.append(node)
            node = came_from[node]
        path.append(self.grid)
        path.reverse()
        print("chemin issu de A*")

        return (time.time() - start_time, len(path) - 1 , path)
    

    def a_star_ancienne_heuristique(self): #ne fonctionnera uniquement pour swap_puzzle
        start_time = time.time()
        goal = Grid(self.grid.m,self.grid.n) 
        frontier = []
        heapq.heappush(frontier, (0, self.grid))  # (priority, node)
        came_from = {}
        cost_so_far = {}
        came_from[self.grid] = None
        cost_so_far[self.grid] = 0
        while len(frontier) > 0 :
            current_cost, current_node = heapq.heappop(frontier)
            if current_node == goal:
                break
            for next_node in current_node.grid_possible(): # Accéder à la liste des voisins du nœud actuel dans le graphe
                new_cost = cost_so_far[current_node] + 1  # On suppose que le coût de chaque mouvement est 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + next_node.heuristique()                    
                    heapq.heappush(frontier, (priority, next_node))
                    came_from[next_node] = current_node
        path = []
        node = goal
        while node != self.grid:
            path.append(node)
            node = came_from[node]
        path.append(self.grid)
        path.reverse()
        print("chemin issu de A*")

        return (time.time() - start_time, len(path) - 1 , path)

    

    @classmethod
    def display(cls, tuple, displayGrid = False): 
        print("Nb of swap : %s" %tuple[1])
        print("Time : %s" %tuple[0])
        if (displayGrid):
            for grid in tuple[2]:
                print(grid)
