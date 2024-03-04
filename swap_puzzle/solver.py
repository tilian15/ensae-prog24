from grid import Grid
import matplotlib.pyplot as plt
from matplotlib.table import Table

def etat_possible2(self):
        l=[]
        for j in range(len(self)):
            for i in range(len(self[0])):
                self.swap((j,i+1),(j,i))
                
                a = [row[:] for row in self.state]
                #print(a)
                l.append(a)  #probleme (résolu), le a qui est ajouté a la liste n'est pas le meme que celui afficher au dessus, pb resolu grace a une copie de self.state
                self.swap((j,i+1),(j,i))
        for y in range(len(self.state[0])):
            for k in range(len(self.state)-1):
                self.swap((k+1,y),(k,y))
                a = [row[:] for row in self.state]
                l.append(a)
                self.swap((k+1,y),(k,y))
        return l


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
        print("From "  + str(self.grid.state) + ' to ' + str(dst.grid.state))
        nodes_done = []
        nodes_todo = [self.grid.state]
        predecessors = {}
        predecessors = {self.grid.state: 0}
        #if we found the dst
        found = False           
        while len(nodes_todo)>0 and not found :             
            node_to_analyse = nodes_todo.pop(0) 
            for n in etat_possible2(node_to_analyse):
                if n not in nodes_done:
                    if (n not in nodes_todo) :
                        nodes_todo.append(n)
                        predecessors[n] = node_to_analyse
                    #to exit the while
                    if (n == dst):
                        found = True

            nodes_done.append(node_to_analyse)
        if not found:
            return None 
                   
        print ('Predecessors-----------')
        print(predecessors)

            
            
        result = []            
        previous = dst
        while (predecessors[previous] != 0):
            result.append(previous)
            previous = predecessors[previous]
        result.append(previous)

            
        result.reverse()
        return result
    # complexité (n+m)*n*m

    


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