import pygame
import sys
import os
import random
import grid as gridLib
from solver import Solver
from PIL import Image

# Définition des couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 200, 250)
DARK_BLUE = (40, 50, 130)
GREEN = (0, 255, 0)

class CaseNum:
    def __init__(self, image_path, grid, nb_row, nb_column, tile_size):
        self.image_path = image_path
        self.tiles = self.split_image(image_path)
        self.grid = grid.state
        self.nb_row = nb_row
        self.nb_column = nb_column
        self.tile_size = tile_size

        print("--GRID DANS INIT--")
        print(self.grid)


    def split_image(self, image_path):
        image = Image.open(image_path)
        width, height = image.size
        tile_width = width // nb_column
        tile_height = height // nb_row

        tiles = []
        for y in range(nb_row):
            for x in range(nb_column):
                box = (x * tile_width, y * tile_height, (x + 1) * tile_width, (y + 1) * tile_height)
                tile = image.crop(box)
                tiles.append(tile)
        return tiles

    # def create_grid(self):
    #     grid = [[0 for _ in range(nb_column)] for _ in range(nb_row)]
    #     numbers = list(range(1, nb_row * nb_column))
    #     random.shuffle(numbers)
    #     index = 0
    #     for i in range(nb_row):
    #         for j in range(nb_column):
    #             if index < len(numbers):
    #                 grid[i][j] = numbers[index]
    #                 index += 1
    #     return grid

    def draw_grid(self, screen, position):
        for row in range(nb_row):
            for column in range(nb_column):
                pygame.draw.rect(screen, DARK_BLUE, (column * self.tile_size + position[0], row * self.tile_size + position[1], self.tile_size, self.tile_size), 1)

                index = self.grid[row][column]
                # image = pygame.image.frombuffer(self.tiles[index].tobytes(), self.tiles[index].size, self.tiles[index].mode)
                # image = pygame.transform.scale(image, (self.tile_size, self.tile_size))

                # screen.blit(image, (column * self.tile_size, row * self.tile_size))

                font = pygame.font.Font(None, 20)
                number_text = font.render(str(self.grid[row][column]), True, DARK_BLUE)
                text_rect = number_text.get_rect(center=(column * self.tile_size + self.tile_size // 2 + position[0], row * self.tile_size + self.tile_size // 2 + position[1]))
                screen.blit(number_text, text_rect)

    def handle_click(self, first_tile_position, second_tile_position):
        row1, col1 = first_tile_position
        row2, col2 = second_tile_position
        self.grid[row1][col1], self.grid[row2][col2] = self.grid[row2][col2], self.grid[row1][col1]

class SwapGenerator:
    def generate_swaps(self, num_swaps, nb_row, nb_column):
        swaps = []
        for _ in range(num_swaps):
            row = random.randint(0, nb_row - 2)
            col = random.randint(0, nb_column - 2)  # Limite de la colonne pour permettre les échanges adjacents
            direction = random.choice(['horizontal', 'vertical'])  # Choisir aléatoirement la direction de l'échange
            if direction == 'horizontal':
                swap1 = (row, col)
                swap2 = (row, col + 1)
            else:
                swap1 = (row, col)
                swap2 = (row + 1, col)
            swaps.append((swap1, swap2))
        return swaps

if __name__ == "__main__":
    NB_ROW = 3  # Nombre de lignes
    NB_COLUMN = 4  # Nombre de colonnes
    nb_row = NB_ROW
    nb_column = NB_COLUMN
    
    # SCREEN_WIDTH = 100*nb_column
    # SCREEN_HEIGHT = 100*nb_row
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800

    TILE_SIZE = 50#SCREEN_WIDTH // nb_column

    # grid = gridLib.Grid(nb_row,nb_column, [[1,5,6],[2,3,4],[7,9,10],[11,12,8]])

    # swaps = [((0,0),(1,0)),((1,2),(1,1))]
    swap_generator = SwapGenerator()
    nb_swaps = 3
    swaps = swap_generator.generate_swaps(nb_swaps, nb_row, nb_column)
    print(swaps)

    # grid = gridLib.Grid(nb_row,nb_column)
    # grid.swap_seq(swaps)

    grid_aff = gridLib.Grid(nb_row,nb_column)
    grid_aff.swap_seq(swaps)

    grid_naive = gridLib.Grid(nb_row,nb_column)
    grid_naive.swap_seq(swaps)
    
    grid_bfs2 = gridLib.Grid(nb_row,nb_column)
    grid_bfs2.swap_seq(swaps)
    
    grid_a_star = gridLib.Grid(nb_row,nb_column)
    grid_a_star.swap_seq(swaps)


    # Initialisation de Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(f"Jeu des cases numérotées {nb_row}x{nb_column}")

    # Initialiser la classe CaseNum avec le chemin de l'image
    image_path = "C:\\Users\\celin\\OneDrive\\Bureau\\python\\nice.jpg"
    case_num = CaseNum(image_path, grid_aff, nb_row, nb_column, TILE_SIZE)

    #    gridTarget = gridLib.Grid(nb_row,nb_column)

    solver = Solver(grid_naive)
    a_naive = solver.get_solution_naive()
    
    solver = Solver(grid_bfs2)
    a_bfs2 = solver.bfs2()
    solver = Solver(grid_a_star)
    # a_star = solver.a_star()
    
    print("-----------------get_solution_naive-----------"+str(len(a_naive)))
    print(a_naive)
    print("-----------------bfs2-----------"+str(len(a_bfs2)))
    print(a_bfs2)
    # print("-----------------a_star-----------"+str(len(a_star)))
    # print(a_star)
    
    print("-+--------------------------")
    print(grid_aff)
    print("-+--------------------------")
    print(swaps)
    # Variables pour le clic de souris
    first_tile_position = None
    position = (50,50)
        
    # Boucle principale du jeu
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Ajuster les coordonnées de la souris en fonction de la taille des tuiles
                column = (mouse_x - position[0]) // TILE_SIZE
                row = (mouse_y - position[1]) // TILE_SIZE

                # column = mouse_x // TILE_SIZE
                # row = mouse_y // TILE_SIZE 
                if 0 <= row < nb_row and 0 <= column < nb_column:  # Vérifier les limites
                    if first_tile_position is not None:
                        # Vérifier si la position actuelle est adjacente à la première position cliquée
                        if (abs(row - first_tile_position[0]) == 1 and column == first_tile_position[1]) or \
                                (row == first_tile_position[0] and abs(column - first_tile_position[1]) == 1):
                            # Effectuer l'échange de cases ici
                            case_num.handle_click(first_tile_position, (row, column))
                            first_tile_position = None  # Réinitialiser la position du premier tile
                    else:
                        first_tile_position = (row, column)  # Stocker la position du premier tile

        # Effacer l'écran et dessiner la grille
        screen.fill(WHITE)
        case_num.draw_grid(screen, position)
        if first_tile_position is not None:
                pygame.draw.rect(screen, GREEN, (first_tile_position[1] * TILE_SIZE + position[0], 
                                                 first_tile_position[0] * TILE_SIZE + position[1], TILE_SIZE, TILE_SIZE))
                font = pygame.font.Font(None, 20)
                white_number_text = font.render(str(case_num.grid[first_tile_position[0]][first_tile_position[1]]), True, WHITE)
                text_rect = white_number_text.get_rect(center=(first_tile_position[1] * TILE_SIZE + TILE_SIZE // 2 + position[0], 
                                                               first_tile_position[0] * TILE_SIZE + TILE_SIZE // 2 + position[1]))
                screen.blit(white_number_text, text_rect)
        
        
        # Affichage de la grille ordonnée en bas à gauche
        ordered_grid = [[i * nb_column + j + 1 for j in range(nb_column)] for i in range(nb_row)]
        tile_size_ordered = 50

        position_ordered = (50,500)
        for row in range(nb_row):
            for column in range(nb_column):
                pygame.draw.rect(screen, DARK_BLUE, (column * tile_size_ordered + position_ordered[0], row * tile_size_ordered + position_ordered[1], tile_size_ordered, tile_size_ordered), 1)

                font = pygame.font.Font(None, 20)
                number_text = font.render(str(ordered_grid[row][column]), True, DARK_BLUE)
                text_rect = number_text.get_rect(center=(column * tile_size_ordered + tile_size_ordered // 2 + position_ordered[0], 
                                                         row * tile_size_ordered + tile_size_ordered // 2 + position_ordered[1]))
                screen.blit(number_text, text_rect)

        position_column_droite = 400
        font = pygame.font.Font(None, 20)
        nb_swaps_text = font.render(f"Nombre de swaps : {nb_swaps}", True, BLACK)
        screen.blit(nb_swaps_text, (position_column_droite, 50))
        
        swaps_text = font.render(f"Swaps : {swaps}", True, BLACK)
        screen.blit(swaps_text, (position_column_droite, 100))

        naive_text = font.render(f"Solution naive : {len(a_naive)}", True, BLACK)
        screen.blit(naive_text, (position_column_droite, 150))

        naive_swap_text = font.render(f"Swaps : {a_naive}", True, BLACK)
        screen.blit(naive_swap_text, (position_column_droite, 200))
        
        bfs2_text = font.render(f"Solution BFS2 : {len(a_bfs2)-1}", True, BLACK)
        screen.blit(bfs2_text, (position_column_droite, 250))

        bfs2_swap_text = font.render(f"Swaps : {a_bfs2}", True, BLACK)
        screen.blit(bfs2_swap_text, (position_column_droite, 300))



        pygame.display.flip()




