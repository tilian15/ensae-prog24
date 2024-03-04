"""
This is the graph module. It contains a minimalistic Graph class.
"""
# from grid import get_grid_from_hashfinal
#from grid import Grid 
import grid
# from grid import get_grid_from_hash2


# def heuristique(self):
#         cpt=0
#         indice=0
#         for i in range(len(self)):
#             for j in range(len(self[0])):
#                 indice+=1
#                 if self[i][j]!=indice : 
#                     cpt+=1


import heapq
class Graph:
    """
    A class representing undirected graphs as adjacency lists. 

    Attributes: 
    -----------
    nodes: NodeType
        A list of nodes. Nodes can be of any immutable type, e.g., integer, float, or string.
        We will usually use a list of integers 1, ..., n.
    graph: dict
        A dictionnary that contains the adjacency list of each node in the form
        graph[node] = [neighbor1, neighbor2, ...]
    nb_nodes: int
        The number of nodes.
    nb_edges: int
        The number of edges. 
    edges: list[tuple[NodeType, NodeType]]
        The list of all edges
    """

    def __init__(self, nodes=[]):
        """
        Initializes the graph with a set of nodes, and no edges. 

        Parameters: 
        -----------
        nodes: list, optional
            A list of nodes. Default is empty.
        """
        self.nodes = nodes 
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
        self.edges = []
        
    def __str__(self):
        """
        Prints the graph as a list of neighbors for each node (one per line)
        """
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output

    def __repr__(self): 
        """
        Returns a representation of the graph with number of nodes and edges.
        """
        return f"<graph.Graph: nb_nodes={self.nb_nodes}, nb_edges={self.nb_edges}>"

    def add_edge(self, node1, node2):
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes. 
        When adding an edge between two nodes, if one of the ones does not exist it is added to the list of nodes.

        Parameters: 
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        """
        if node1 not in self.graph:
            self.graph[node1] = []
            self.nb_nodes += 1
            self.nodes.append(node1)
        if node2 not in self.graph: #j'ai decommenter ??? 
            self.graph[node2] = []
            self.nb_nodes += 1
            self.nodes.append(node2)
        if node2 not in self.graph[node1]: #rajout de cette ligne pour éviter les doublons 

            self.graph[node1].append(node2)
        if node1 not in self.graph[node2]: #idem
            self.graph[node2].append(node1)
        self.nb_edges += 1
        self.edges.append((node1, node2))

    def bfs(self, src, dst): 
        """
        Finds a shortest path from src to dst by BFS.  

        Parameters: 
        -----------
        src: NodeType
            The source node.
        dst: NodeType
            The destination node.

        Output: 
        -------
        path: list[NodeType] | None
            The shortest path from src to dst. Returns None if dst is not reachable from src
        """
        dist=[-1 for i in range(max(self.nodes))]  #ce n'est pas la meilleure implémentation car on crée un tableau énorme donc on cherche à faire autrement plus tard(cf bfs2)
        deja_traiter=[False for i in range(max(self.nodes))]
        pred = [src for i in range(max(self.nodes))]
        a_traiter=[]  
        deja_traiter[src-1]=True
        a_traiter.append(src)
        dist[src-1]=0
        found = False
        while len(a_traiter)>0 and not found:
            y= a_traiter.pop(0)
            for t in self.graph[y]:
                if not(deja_traiter[t-1]):
                    deja_traiter[t-1]=True
                    a_traiter.append(t)
                    dist[t-1]=dist[y-1]+1
                    pred[t-1]=y
                if t == dst:
                    found = True 
        a=dst
        plus_court_chemin=[dst]
        print(plus_court_chemin)
        print("toto")
        print(pred[a-1], src, dst)
        
       # print(pred[645312-1])
        if pred[a-1]!= src : #on effectue le chemin inverse pour trouver le chemin
            while pred[a-1]!=src:
                a=pred[a-1]
                plus_court_chemin.append(a)
            plus_court_chemin.append(src)
            plus_court_chemin.reverse()
            return plus_court_chemin
        else : 
            return [src, dst] #if src == dst else None #dst n'est pas atteignable
        # print(plus_court_chemin)
        # print("toto")
        # if pred[a]!=src : 
        #     while pred[a]!=src:
        #         a=pred[a]
        #         plus_court_chemin.append(a)
        #     plus_court_chemin.append(src)
        #     plus_court_chemin.reverse()
        #     return plus_court_chemin
        # else : 
        #     return [src, dst] if src == dst else None #dst n'est pas atteignable  



    def bfs2(self, src, dst): #on cherche à implémenter cette fonction pour trouver une alternative et éviter de créer un tableau de taille len(max) mais pour le moment le plus court chemin n'est pas optimal 
            
        print("From "  + str(src) + ' to ' + str(dst))
        nodes_done = []
        nodes_todo = [src]
        predecessors = {}
        predecessors = {src: 0}
        #if we found the dst
        found = False           
        while len(nodes_todo)>0 and not found :
                         
            node_to_analyse = nodes_todo.pop(0) 
            for n in self.graph[node_to_analyse]:
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

    def a_star(self, start, goal): #ne fonctionnera uniquement pour swap_puzzle
        frontier = []
        heapq.heappush(frontier, (0, start))  # (priority, node)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while frontier:
            current_cost, current_node = heapq.heappop(frontier)

            if current_node == goal:
                break

            for next_node in self.graph[current_node]: # Accéder à la liste des voisins du nœud actuel dans le graphe
                new_cost = cost_so_far[current_node] + 1  # On suppose que le coût de chaque mouvement est 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    print('caca')
                    priority = new_cost + grid.pbo_get_grid_from_hash(next_node).heuristique()
                    #priority = new_cost + get_grid_from_hash2(next_node).heuristique2()
                    heapq.heappush(frontier, (priority, next_node))
                    came_from[next_node] = current_node

    # Reconstruct path
        path = []
        node = goal
        while node != start:
            path.append(node)
            node = came_from[node]
        path.append(start)
        path.reverse()

        return path

            





    @classmethod
    def graph_from_file(cls, file_name):
        """
        Reads a text file and returns the graph as an object of the Graph class.

        The file should have the following format: 
            The first line of the file is 'n m'
            The next m lines have 'node1 node2'
        The nodes (node1, node2) should be named 1..n

        Parameters: 
        -----------
        file_name: str
            The name of the file

        Outputs: 
        -----------
        graph: Graph
            An object of the class Graph with the graph from file_name.
        """
        with open(file_name, "r") as file:
            n, m = map(int, file.readline().split())
            graph = Graph(range(1, n+1))
            for _ in range(m):
                edge = list(map(int, file.readline().split()))
                if len(edge) == 2:
                    node1, node2 = edge
                    graph.add_edge(node1, node2) # will add dist=1 by default
                else:
                    raise Exception("Format incorrect")
        return graph

