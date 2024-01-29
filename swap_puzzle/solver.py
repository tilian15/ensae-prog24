from grid import Grid
import matplotlib.pyplot as plt
from matplotlib.table import Table

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