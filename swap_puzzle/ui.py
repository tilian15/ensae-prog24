import random
import os
import pygame
import pygame_gui
from collections import deque

from pygame_gui import UIManager, PackageResource

from pygame_gui.elements import UIWindow
from pygame_gui.elements import UIButton
from pygame_gui.elements import UIHorizontalSlider
from pygame_gui.elements import UITextEntryLine
from pygame_gui.elements import UIDropDownMenu
from pygame_gui.elements import UIScreenSpaceHealthBar
from pygame_gui.elements import UILabel
from pygame_gui.elements import UIImage
from pygame_gui.elements import UIPanel
from pygame_gui.elements import UISelectionList
from pygame_gui.elements import UITextBox
from pygame_gui.windows import UIMessageWindow

import grid as gridLib
from solver import Solver

import pygame

TILE_SIZE = 50
POSITION = (50, 500)
FIRST_TILE_POSITION = None
        
class SwapGenerator:
    def generate_swaps(self, num_swaps, nb_lignes, nb_col): #nous permet de generer les swaps à réaliser pour rendre une grille aléatoire 
        swaps = []
        for _ in range(num_swaps):
            row = random.randint(0, nb_lignes - 2)
            col = random.randint(0, nb_col - 2)  # Limite de la colonne pour permettre les échanges adjacents
            direction = random.choice(['horizontal', 'vertical'])  # Choisir aléatoirement la direction de l'échange
            if direction == 'horizontal':
                swap1 = (row, col)
                swap2 = (row, col + 1)
            else:
                swap1 = (row, col)
                swap2 = (row + 1, col)
            swaps.append((swap1, swap2))
        return swaps
    
class CaseNum:
    def __init__(self, grid, nb_lignes, nb_col, tile_size, puzzleWin, ui_manager):
        self.nb_lignes = nb_lignes
        self.nb_col = nb_col
        self.tile_size = tile_size
        self.grid = grid.state
        self.puzzleWin = puzzleWin
        self.ui_manager = ui_manager
        
    def draw_grid(self, position):                             
        for row in range(self.nb_lignes):
            for column in range(self.nb_col):
                # pygame.draw.rect(screen, (204, 204, 204), (column * self.tile_size + position[0], row * self.tile_size + position[1], self.tile_size, self.tile_size), 1)
                # font = pygame.font.Font(None, 20)
                # number_text = font.render(str(self.grid[row][column]), True, (204, 204, 204))
                # text_rect = number_text.get_rect(center=(column * self.tile_size + self.tile_size // 2 + position[0], row * self.tile_size + self.tile_size // 2 + position[1]))
                # screen.blit(number_text, text_rect)
                button = UIButton(
                    pygame.Rect(column * self.tile_size + position[0],row * self.tile_size + position[1],self.tile_size,self.tile_size),
                    str(self.grid[row][column]),
                    self.ui_manager,container=self.puzzleWin,object_id='#disable_button',  
                )
                button.set_relative_position(
                    (column * self.tile_size + self.tile_size // 2 + position[0], 
                     row * self.tile_size + self.tile_size // 2 + position[1])
                )
               

    def handle_click(self, first_tile_position, second_tile_position):
        row1, col1 = first_tile_position
        row2, col2 = second_tile_position
        self.grid[row1][col1], self.grid[row2][col2] = self.grid[row2][col2], self.grid[row1][col1]

class PuzzleWindow(UIWindow):
    def __init__(self, rect, ui_manager, nb_lignes, nb_col, nb_swaps):
        super().__init__(rect, ui_manager,
                         window_display_title='SWAP PUZZLE : Comparaison d\'algorithmes',
                         object_id='#everything_window',
                         resizable=True,
                         element_id='puzzle')

        self.nb_lignes = nb_lignes
        self.nb_col = nb_col
        self.nb_swaps = nb_swaps

        self.options = Options()
        self.titre = UILabel(pygame.Rect(self.options.resolution[0] /2,20,750,44),"Comparaison d'algorithmes",self.ui_manager,object_id='#titre',container=self)
        label_position = pygame.math.Vector2((self.options.resolution[0] - self.titre.rect.width) // 2, 20) # centre en largeur
        self.titre.set_relative_position(label_position)

        swap_generator = SwapGenerator()
        swaps = swap_generator.generate_swaps(self.nb_swaps, self.nb_lignes, self.nb_col)
        text_swaps = ''
        for grid in swaps:
            text_swaps += str(grid) + '<br>'

        UITextBox(f'<b>Nombre de colonnes :</b> {self.nb_col}'
                    '<br>'
                    f'<b>Nombre de lignes :</b> {self.nb_lignes}'
                    '<br>'
                    f'<b>Nombre de swaps :</b> {self.nb_swaps}'
                    '<br>'
                    f'Swaps : <br>{text_swaps}'
                    '<br>'
                    '',
                    pygame.Rect((50, int(self.options.resolution[1] * 0.15)), (250, 300)),self.ui_manager,object_id='text_box',
                                            container=self)
        
        gOriginal = gridLib.Grid(self.nb_lignes, self.nb_col)
        gOriginal.swap_seq(swaps)

        case_num = CaseNum(gOriginal, self.nb_lignes, self.nb_col, TILE_SIZE, self, self.ui_manager)
        case_num.draw_grid(POSITION)

        result = self.start_algo(gOriginal)
        self.display_results(result)

        
    def display_results(self, result):
        a_naive = result[0]
        a_bfs2 = result[1]
        a_star = result[2]

        text_a_naive = ''
        for grid in a_naive[2]:
            text_a_naive += str(grid.state) + '<br>'
        
        text_a_bfs2 = ''
        for grid in a_bfs2[2]:
            text_a_bfs2 += str(grid.state) + '<br>'

        text_a_star = ''
        for grid in a_star[2]:
            text_a_star += str(grid.state) + '<br>'

        UITextBox('<b> Méthode naïve :</b>'
            f'<i>{a_naive[1]} swaps en {a_naive[0]}s</i>'
            '<br>'
            f'{text_a_naive}'
            '<br>'
            '<b> Méthode BSF2 :</b>'
            f'<i>{a_bfs2[1]} swaps en {a_bfs2[0]}s</i>'
            '<br>'
            f'{text_a_bfs2}'
            '<br>'
            '<b> Méthode A* :</b>'
            f'<i>{a_star[1]} swaps en {a_star[0]}s</i>'
            '<br>'
            f'{text_a_star}'
            '<br>'
            '<br>'
            '',
            pygame.Rect((self.options.resolution[0] /2-50, int(self.options.resolution[1] * 0.15)), 
                        (self.options.resolution[0] /2-50, self.options.resolution[1]-100)),
                        self.ui_manager,object_id='#text_box_trans',
                        container=self)

    def start_algo(self, gOriginal):
        grid_naive = gOriginal.clone()
        grid_bfs2 = gOriginal.clone()
        grid_a_star = gOriginal.clone()

        display_grid_result = False
        solver = Solver(grid_naive)
        a_naive = solver.get_solution_naive()
        print("Naive")
        Solver.display(a_naive, display_grid_result)


        solver = Solver(grid_a_star)
        a_star = solver.a_star()
        print("A*")
        Solver.display(a_star, display_grid_result)

        solver = Solver(grid_bfs2)
        a_bfs2 = solver.bfs2_optimise()
        print("BF2")
        Solver.display(a_bfs2, display_grid_result)

        result = []
        result.append(a_naive)
        # result.append(a_naive)
        # result.append(a_naive)
        
        result.append(a_bfs2)
        result.append(a_star)

        return result
        
    def update(self, time_delta):
        super().update(time_delta)


class Options:
    def __init__(self):
        self.resolution = (800, 800)
        self.fullscreen = False

class OptionsUIApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("SWAP PUZZLE : Configuration")
        self.options = Options()
        if self.options.fullscreen:
            self.window_surface = pygame.display.set_mode(self.options.resolution,
                                                          pygame.FULLSCREEN)
        else:
            self.window_surface = pygame.display.set_mode(self.options.resolution)

        self.background_surface = None

        self.ui_manager = UIManager(self.options.resolution,
                                    PackageResource(package='data.themes',
                                                    resource='theme_2.json'))
        self.ui_manager.preload_fonts([{'name': 'fira_code', 'point_size': 10, 'style': 'bold'},
                                       {'name': 'fira_code', 'point_size': 10, 'style': 'regular'},
                                       {'name': 'fira_code', 'point_size': 10, 'style': 'italic'},
                                       {'name': 'fira_code', 'point_size': 14, 'style': 'italic'},
                                       {'name': 'fira_code', 'point_size': 14, 'style': 'bold'}
                                       ])

        self.test_button_go = None
        self.test_text_down_nb_ligne = None
        self.test_drop_down_nb_ligne= None
        self.test_text_down_nb_colonne= None
        self.test_drop_down_nb_colonne= None
        self.panel = None
        self.titre = None
        self.swap_selection = None

        self.message_window = None

        self.recreate_ui()

        self.clock = pygame.time.Clock()
        self.time_delta_stack = deque([])

        self.button_response_timer = pygame.time.Clock()
        self.running = True
        self.debug_mode = False

        self.all_enabled = True
        self.all_shown = True

    def recreate_ui(self):
        self.ui_manager.set_window_resolution(self.options.resolution)
        self.ui_manager.clear_and_reset()

        self.background_surface = pygame.Surface(self.options.resolution)
        self.background_surface.fill(self.ui_manager.get_theme().get_colour('dark_bg'))

        self.test_button_go = UIButton(pygame.Rect((int(self.options.resolution[0] / 2),int(self.options.resolution[1] * 0.50)),(110, 40)),
                                      'GO',
                                      self.ui_manager,
                                      object_id='#disable_button')

        self.test_text_down_nb_colonne = UILabel(pygame.Rect(self.options.resolution[0] /2-100,int(self.options.resolution[1] * 0.25),200,27),
                                                 "Nombre de colonnes",
                                                 self.ui_manager,
                                                 object_id='#label')
                    
        self.test_text_down_nb_ligne = UILabel(pygame.Rect(self.options.resolution[0] /2-100,int(self.options.resolution[1] * 0.3),200,27),
                                                "Nombre de lignes",
                                                self.ui_manager,
                                                object_id='#label')
                                        
        self.test_drop_down_nb_ligne= UIDropDownMenu([ '2', '3', '4', '5'],'3',
                                             pygame.Rect((int(self.options.resolution[0] / 2+100),int(self.options.resolution[1] * 0.3)),(200, 25)),
                                             self.ui_manager)
        
        self.test_drop_down_nb_colonne = UIDropDownMenu(['2', '3', '4', '5'],'3',
                                                        pygame.Rect((int(self.options.resolution[0] / 2+100),int(self.options.resolution[1] * 0.25)),(200, 25)),
                                                        self.ui_manager)

        self.panel = UIPanel(pygame.Rect(50, 120, 200, 270),
                             starting_height=4,
                             manager=self.ui_manager)

        UIButton(pygame.Rect(10, 10, 174, 30), 'Nombre de swaps',
                 manager=self.ui_manager,
                 container=self.panel)

        self.swap_selection = UISelectionList(pygame.Rect(10, 50, 174, 200),
                                              item_list=['1','2','3','4','5','6','7','8','9','10',
                                                         '11','12','13','14','15','16','17','18','19','20'],
                                                         manager=self.ui_manager,
                                                         container=self.panel,
                                                         allow_multi_select=False, 
                                                         default_selection='5' )

        self.titre = UILabel(pygame.Rect(self.options.resolution[0] /2,20,230,44),"SWAP PUZZLE",self.ui_manager,object_id='#titre')

        # Centrer le UILabel dans la fenêtre
        self.options = Options() 
        label_position = pygame.math.Vector2((self.options.resolution[0] - self.titre.rect.width) // 2, 20) # centre en largeur
        self.titre.set_relative_position(label_position)

    def change_ligne_colonne(self):
        print(f"NB Colonne : {self.test_drop_down_nb_colonne.selected_option}")
        print(f"NB Lignes : {self.test_drop_down_nb_ligne.selected_option}")
        selected_index = self.swap_selection.get_single_selection()
        if selected_index is not None:
            selected_value = self.swap_selection.item_list[int(selected_index)]
            print(f"NB Swaps : {int(selected_value['text'])-1 }")

    def process_events(self):
        global FIRST_TILE_POSITION
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.ui_manager.process_events(event)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.test_button_go:
    
                    selected_index = self.swap_selection.get_single_selection()
                    if selected_index is not None:
                        selected_value = self.swap_selection.item_list[int(selected_index)]
                        nb_swaps = int(selected_value['text'])-1

                    nb_lignes = int(self.test_drop_down_nb_ligne.selected_option)
                    nb_col = int(self.test_drop_down_nb_colonne.selected_option)
                    PuzzleWindow(pygame.Rect((5, 5), (800, 800)), self.ui_manager, nb_lignes, nb_col, nb_swaps)

            if (event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED
                    and (event.ui_element == self.test_drop_down_nb_colonne 
                         or event.ui_element == self.test_drop_down_nb_ligne)):
                self.change_ligne_colonne()

            if (event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION
                and event.ui_element == self.swap_selection):
                self.change_ligne_colonne()

            # if event.type == pygame.MOUSEBUTTONDOWN:
                # mouse_x, mouse_y = pygame.mouse.get_pos()
                # column = (mouse_x - POSITION[0]) // TILE_SIZE
                # row = (mouse_y - POSITION[1]) // TILE_SIZE
                # nb_col = self.test_drop_down_nb_colonne.selected_option
                # nb_lignes = self.test_drop_down_nb_ligne.selected_option
                # if 0 <= row < int(nb_lignes) and 0 <= column < int(nb_col):  # Vérifier les limites
                #     if FIRST_TILE_POSITION is not None:
                #         # Vérifier si la position actuelle est adjacente à la première position cliquée
                #         if (abs(row - FIRST_TILE_POSITION[0]) == 1 and column == FIRST_TILE_POSITION[1]) or \
                #                 (row == FIRST_TILE_POSITION[0] and abs(column - FIRST_TILE_POSITION[1]) == 1):
                #             # Effectuer l'échange de cases ici


                #             #  A decommenter        case_num.handle_click(first_tile_position, (row, column))
                #             FIRST_TILE_POSITION = None  # Réinitialiser la position du premier tile
                #     else:
                #         print('ICI')
                #         FIRST_TILE_POSITION = (row, column)  # Stocker la position du premier tile

    def run(self):
        while self.running:
            time_delta = self.clock.tick() / 1000.0
            self.time_delta_stack.append(time_delta)
            if len(self.time_delta_stack) > 2000:
                self.time_delta_stack.popleft()

            # check for input
            self.process_events()

            # respond to input
            self.ui_manager.update(time_delta)

            # draw graphics
            self.window_surface.blit(self.background_surface, (0, 0))
            self.ui_manager.draw_ui(self.window_surface)

            pygame.display.update()


if __name__ == '__main__':
    app = OptionsUIApp()
    app.run()
