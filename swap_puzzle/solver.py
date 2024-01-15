from grid import Grid

class Solver(Grid): 
    """
    A solver class, to be implemented.
    """

    def __init__(self):
        super().__init__


    def coordonne(self,a):
        for i in range(self.state):
            for j in range(self.state[0]):
                if self.state[i][j]==a : 
                    return (j,i)
    
    def get_solution(self):
        """
        Solves the grid and returns the sequence of swaps at the format 
        [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...]. 
        """

        # TODO: implement this function (and remove the line "raise NotImplementedError").
        # NOTE: you can add other methods and subclasses as much as necessary. The only thing imposed is the format of the solution returned.
       

