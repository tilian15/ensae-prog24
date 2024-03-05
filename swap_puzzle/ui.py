import pygame
import sys
import os
import random
import grid as gridLib
from solver import Solver
from PIL import Image
import re

# Définition des couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 200, 250)
DARK_BLUE = (40, 50, 130)
GREEN = (0, 255, 0)
ARIAL = os.path.join(os.environ["SystemRoot"], "Fonts", "arial.ttf")


class CaseNum:
    def __init__(self, image_path, grid, nb_row, nb_column, tile_size):
        self.image_path = image_path
        self.nb_row = nb_row
        self.nb_column = nb_column
        self.tile_size = tile_size

        # self.tiles = self.split_image(image_path)
        self.grid = grid.state
        

    # def split_image(self, image_path):
    #     image = Image.open(image_path)
    #     width, height = image.size
    #     tile_width = width // self.nb_column
    #     tile_height = height // self.nb_row

    #     tiles = []
    #     for y in range(self.nb_row):
    #         for x in range(self.nb_column):
    #             box = (x * tile_width, y * tile_height, (x + 1) * tile_width, (y + 1) * tile_height)
    #             tile = image.crop(box)
    #             tiles.append(tile)
    #     return tiles


    def draw_grid(self, screen, position):
        for row in range(self.nb_row):
            for column in range(self.nb_column):
                # tile_rect = pygame.Rect(column * self.tile_size + position[0], row * self.tile_size + position[1], self.tile_size, self.tile_size)
                # pygame.draw.rect(screen, BLACK, tile_rect, 1)  # Dessiner une bordure noire autour de la tuile
                pygame.draw.rect(screen, DARK_BLUE, (column * self.tile_size + position[0], row * self.tile_size + position[1], self.tile_size, self.tile_size), 1)

                # index = self.grid[row][column]
                # if 0 <= index < len(self.tiles):  # Vérifier si l'indice est valide
                #     image = pygame.image.frombuffer(self.tiles[index].tobytes(), self.tiles[index].size, self.tiles[index].mode)
                #     image = pygame.transform.scale(image, (self.tile_size, self.tile_size))

                #     # Calculer la position d'affichage de l'image en fonction de la position globale de la grille
                #     display_position = (column * self.tile_size + position[0], row * self.tile_size + position[1])
                #     screen.blit(image, display_position)

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

def restart_game(gOriginal, grid_naive, grid_bfs2, grid_a_star, swaps, nb_swaps, nb_row, nb_column):
    print("RESTARTTTTT")
    swap_generator = SwapGenerator()
    swaps = swap_generator.generate_swaps(nb_swaps, nb_row, nb_column)
    gOriginal.swap_seq(swaps)
    grid_naive.swap_seq(swaps)
    grid_bfs2.swap_seq(swaps)
    grid_a_star.swap_seq(swaps)

    solver = Solver(grid_naive)
    a_naive = solver.get_solution_naive()

    solver = Solver(grid_bfs2)
    a_bfs2 = solver.bfs2()

    return swaps  # Retourner les swaps générés

def main(image_path):
    NB_ROW = 3
    NB_COLUMN = 4
    nb_row = NB_ROW
    nb_column = NB_COLUMN
    nb_swaps = 3
    display_grid_result = False
    
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800

    TILE_SIZE = 50

    swap_generator = SwapGenerator()
    swaps = swap_generator.generate_swaps(nb_swaps, nb_row, nb_column)

    gOriginal = gridLib.Grid(nb_row, nb_column)
    gOriginal.swap_seq(swaps)

    grid_naive = gOriginal.clone()
    grid_bfs2 = gOriginal.clone()
    grid_a_star = gOriginal.clone()

    # Initialisation de Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(f"Jeu des cases numérotées {nb_row}x{nb_column}")

    # Initialiser la classe CaseNum avec le chemin de l'image
    image_path = "C:\\Users\\celin\\OneDrive\\Bureau\\python\\nice.jpg"
    case_num = CaseNum(image_path, gOriginal, nb_row, nb_column, TILE_SIZE)

    solver = Solver(grid_naive)
    a_naive = solver.get_solution_naive()
    Solver.display(a_naive, display_grid_result)

    solver = Solver(grid_bfs2)
    a_bfs2 = solver.bfs2()
    Solver.display(a_bfs2, display_grid_result)

    solver = Solver(grid_a_star)
    a_star = solver.a_star()
    Solver.display(a_star, display_grid_result)

    image_path = "C:\\Users\\celin\\OneDrive\\Bureau\\python\\nice.jpg"
    case_num = CaseNum(image_path, gOriginal, nb_row, nb_column, TILE_SIZE)

    #    gridTarget = gridLib.Grid(nb_row,nb_column) 

    # Variables pour le clic de souris
    first_tile_position = None
    position = (50, 50)

    # Boucle principale du jeu
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                column = (mouse_x - position[0]) // TILE_SIZE
                row = (mouse_y - position[1]) // TILE_SIZE
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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 400 <= mouse_x <= 500 and 350 <= mouse_y <= 400:
                    swaps = restart_game(gOriginal, grid_naive, grid_bfs2, grid_a_star, swaps, nb_swaps, nb_row, nb_column)
                    case_num = CaseNum(image_path, gOriginal, nb_row, nb_column, TILE_SIZE)  # Mettre à jour la grille


        screen.fill(BLUE)
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
        position_ordered = (50, 500)
        for row in range(nb_row):
            for column in range(nb_column):
                pygame.draw.rect(screen, DARK_BLUE, (column * tile_size_ordered + position_ordered[0],
                                                     row * tile_size_ordered + position_ordered[1], tile_size_ordered,
                                                     tile_size_ordered), 1)

                font = pygame.font.Font(None, 25)
                number_text = font.render(str(ordered_grid[row][column]), True, DARK_BLUE)
                text_rect = number_text.get_rect(center=(column * tile_size_ordered + tile_size_ordered // 2 +
                                                         position_ordered[0],
                                                         row * tile_size_ordered + tile_size_ordered // 2 +
                                                         position_ordered[1]))
                screen.blit(number_text, text_rect)
		


        font = pygame.font.Font(ARIAL, 20)
        position_column_right = 400
        x = position_column_right
        y = 50

        text_render = [
            f"Nombre de swaps : {nb_swaps}",
            f"Swaps : {swaps}",
            "",
            f"Solution naïve : {a_naive[1]} swaps en {a_naive[0]}s",

        ]

        for grid in a_naive[2]:
            text_render.append(str(grid.state))

        text_render.append("")
        text_render.append(f"Solution BFS2 : {a_bfs2[1]} swaps en {a_bfs2[0]}s")
        for grid in a_bfs2[2]:
            text_render.append(str(grid.state))

        text_render.append("")
        text_render.append(f"Solution A* : {a_star[1]} swaps en {a_star[0]}s")
        for grid in a_star[2]:
            text_render.append(str(grid.state))
        
        rendered_text = [font.render(line, True, BLACK) for line in text_render]

        # Affichage du texte sur la fenêtre
        for t in rendered_text:
            screen.blit(t, (x, y))
            y += t.get_height() + 5  # Espacement entre les lignes

        # pygame.draw.rect(screen, DARK_BLUE, (position_column_right, 350, 100, 50))
        # restart_font = pygame.font.Font(None, 30)
        # restart_text = restart_font.render("Restart", True, WHITE)
        # screen.blit(restart_text, (position_column_right+20, 365))

        pygame.display.flip()

if __name__ == "__main__":
    image_path = "C:\\Users\\celin\\OneDrive\\Bureau\\python\\nice.jpg"

    main(image_path)
