from grid import Grid
import matplotlib.pyplot as plt
from matplotlib.table import Table
import heapq


def heuristique2(self):
        #self=global_haschage2bis(a)
        cpt=0
        m=len(self) #nbre de ligne
        n = len(self[0]) #nbre de colonne
        for i in range(m):
            for j in range(n):
                a=self[i][j]
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

print(heuristique2([[4,2,3],[1,5,6]]))

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
                a=swap(a,(j,i+1),(j,i))
                b = [row[:] for row in a]
                #print(a)
                l.append(b) 
                a=swap(a,(j,i+1),(j,i))
        for y in range(len(self[0])):
            for k in range(len(self)-1):
                a=swap(a,(k+1,y),(k,y))
                b = [row[:] for row in a]
                l.append(b)
                a=swap(a,(k+1,y),(k,y))
        return l


def global_haschage2(aGrid): #haschage à partir d'une grille grid
    print(aGrid)
    pre =  str(aGrid.m) + ";" +  str(aGrid.n) 
    for i in range(0,aGrid.m):
        for j in range(0,aGrid.n):
            pre = pre + ";" + str(aGrid.state[i][j])
    return pre

def global_haschage2bis(tab): #haschage à partir d'un tablo
    n=len(tab[0])
    m=len(tab)
    pre = str(m) + ';' + str(n)
    for i in range(0,m):
        for j in range(0,n):
            pre = pre + ";" + str(tab[i][j])
    return pre

#print(etat_possible2([[1,2,3],[4,5,6]]))

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
        affichage(self.grid.state)
        sequence = []
        for i in range(1,(self.grid.n * self.grid.m) +1 ):
            print("toto")
            sequence2=[]
            sequence2+=self.grid.bonne_colonne(i)
            #print(f"bonne colonne {i} ok")
            sequence2+=self.grid.bonne_ligne(i)
            #print(f"bonne ligne {i} ok")
            sequence+=sequence2
            if len(sequence2) !=0 : 
                affichage(self.grid.state)
            print(self.grid)
        return sequence
        

    def bfs2(self): #Question 8, ce bfs ne fonctionnera que pour swap_puzzle 
        dst = Grid(self.grid.m,self.grid.n)    
        print("From "  + str(self.grid.state) + ' to ' + str(dst.state))
        nodes_done = []
        nodes_todo = [self.grid.state]
        predecessors = {}
        predecessors = {global_haschage2bis(self.grid.state): 0}
        #if we found the dst
        found = False           
        while len(nodes_todo)>0 and not found :             
            node_to_analyse = nodes_todo.pop(0) 
            for n in etat_possible2(node_to_analyse):
                if n not in nodes_done:
                    if (n not in nodes_todo) :
                        nodes_todo.append(n)
                        predecessors[global_haschage2bis(n)] = node_to_analyse
                    #to exit the while
                    if (n == dst.state):
                        found = True

            nodes_done.append(node_to_analyse)
        if not found:
            return None 
                   
        print ('Predecessors-----------')
        print(predecessors)

            
            
        result = []            
        previous = dst.state
        while (predecessors[global_haschage2bis(previous)] != 0):
            result.append(previous)
            previous = predecessors[global_haschage2bis(previous)]
        result.append(previous)
        result.reverse()
        return result
    # complexité (n+m)*n*m



    def a_star(self): #ne fonctionnera uniquement pour swap_puzzle
        goal = Grid(self.grid.m,self.grid.n) 
        frontier = []
        heapq.heappush(frontier, (0, self.grid.state))  # (priority, node)
        came_from = {}
        cost_so_far = {}
        came_from[global_haschage2bis(self.grid.state)] = None
        cost_so_far[global_haschage2bis(self.grid.state)] = 0

        while len(frontier) > 0 :
            current_cost, current_node = heapq.heappop(frontier)

            if current_node == global_haschage2(goal):
                break

            for next_node in etat_possible2(current_node): # Accéder à la liste des voisins du nœud actuel dans le graphe
                new_cost = cost_so_far[global_haschage2bis(current_node)] + 1  # On suppose que le coût de chaque mouvement est 1
                if global_haschage2bis(next_node) not in cost_so_far or new_cost < cost_so_far[global_haschage2bis(next_node)]:
                    cost_so_far[global_haschage2bis(next_node)] = new_cost
                    print('caca')
                    priority = new_cost + heuristique2(next_node)
                    #priority = new_cost + get_grid_from_hash2(next_node).heuristique2()
                    heapq.heappush(frontier, (priority, next_node))
                    came_from[global_haschage2bis(next_node)] = current_node

    # Reconstruct path
        path = []
        node = goal.state
        while node != self.grid.state:
            path.append(node)
            node = came_from[global_haschage2bis(node)]
        path.append(self.grid.state)
        path.reverse()
        print("chemin issu de A*")

        return path

    


        # TODO: implement this function (and remove the line "raise NotImplementedError").
        # NOTE: you can add other methods and subclasses as much as necessary. The only thing imposed is the format of the solution returned.
       

def affichage(data):
    fig, ax = plt.subplots()
    ax.axis('off')  # Hide axis
    rows, cols = len(data), len(data[0])
    table = Table(ax, bbox=[0, 0, 1, 1], loc='center')

    for i in range(rows):
        for j in range(cols):
            table.add_cell(i, j, 1 / cols, 1 / rows, text=str(data[i][j]), loc='center')


    ax.add_table(table)

    plt.show()