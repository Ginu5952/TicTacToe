import tkinter
from tkinter import messagebox
import pygame
import os
import math


class Gamee(object):
    WINNING_STATES = ((0, 1, 2), (3, 4, 5), (6, 7, 8),  # row
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),  # column
                      (0, 4, 8), (2, 4, 6))  # diagonal

    def __init__(self, parent,first,second):
        parent.title('Tic Tac Toe')
        parent.configure(bg='white')  # Set background color
        parent.option_add('*Font', 'Helvetica 18 bold')
        canvas = tkinter.Canvas(parent, width=600, height=600, bg='lightblue')
        self.first = first
        self.turn_label = tkinter.Label(parent, height=2, text=f"{self.first}.'s turn".capitalize(),
                                        bg='white', fg='blue')
        self.second = second


        turn_label = self.turn_label
        turn_label.grid(row=1, column=0)

        for i in range(3):
            y0 = i * 200
            y1 = (i + 1) * 200
            canvas.create_rectangle(0, y0, 200, y1)
            canvas.create_rectangle(200, y0, 400, y1)
            canvas.create_rectangle(400, y0, 600, y1)
        canvas.grid()
        canvas.bind("<Button-1>", self.play)

        restart_btn = tkinter.Button(parent, text='RESTART', height=2, width=10, command=self.restart)
        restart_btn.grid(row=3, column=0, pady=(25, 10))

       

        # Create a label widget for the win/lose message
        result_string = tkinter.StringVar()
        tkinter.Label(parent, height=2, textvariable=result_string).grid()

        # initialize instance variables
        self.result = result_string  # Tkinter string var to display game result
        self.canvas = canvas  # Tkinter canvas widget object
        self.filled = set()  # filled canvas rectangle object reference
        self.tiles = set(range(9))  # free tiles indices on board board
        self.maxAgent = set()  # maximizing player's filled tiles index
        self.minAgent = set()  # minimizing player's filled tiles index
        self.isMaxAgent = True  # True if player's turn. False, if computer's.
        self.__update_turn_label()
       

    def restart(self):
        # This method is invoked when the user clicks on the RESTART button.
        for filled_tile in self.canvas.find_all():
            self.canvas.itemconfigure(filled_tile, fill='')

        # reinitialize game instance variables
        self.result.set('')
        self.filled = set()
        self.tiles = set(range(9))
        self.maxAgent = set()
        self.minAgent = set()
        self.isMaxAgent = True
        self.__update_turn_label()
       

    def play(self, event):
        if self.result.get() != '':
            return

        tile = (event.y // 200) * 3 + (event.x // 200)
        if tile in self.tiles:
            self.__update_board_canvas(tile)
            play_sound("music/mixkit-arcade-game-jump-coin-216.wav")
            self.__update_game_state(tile)
            self.__update_result_label()
            self.__update_turn_label()
            

    # ------------------------------------------------------------------------
    #  Instance Helper Functions: Updating and Checking Game States
    # ------------------------------------------------------------------------
    def __update_game_state(self, tile):
        try:
            self.tiles.remove(tile)
            if self.isMaxAgent:
                self.maxAgent.add(tile)
            else:
                self.minAgent.add(tile)
            self.isMaxAgent = not self.isMaxAgent
        except KeyError as key_error:
            pass

    # ------------------------------------------------------------------------
    #  Instance Helper Functions: Setting and Getting Board
    # ------------------------------------------------------------------------
    def __update_board_canvas(self, tile):
        if tile not in self.maxAgent and tile not in self.minAgent:
            self.__paint_tile(tile)

    def __update_result_label(self):
        score = Gamee.__evaluate_win(self.maxAgent, self.minAgent)
        if score == 10:
            play_sound("music/mixkit-arcade-bonus-alert-767.wav")
            messagebox.showinfo("Game Over", f"{self.first} Win!".capitalize())
        elif score == -10:
            play_sound("music/mixkit-arcade-bonus-alert-767.wav")
            messagebox.showinfo("Game Over", f"{self.second} Win".capitalize())
        elif score == 0 and len(self.tiles) == 0:
            play_sound("music/mixkit-little-piano-game-over-1944.wav")
            messagebox.showinfo("Game Over", "Draw")

    def __update_turn_label(self):
        if self.isMaxAgent:
            self.turn_label.config(text=f"{self.first}'s turn".capitalize())
        else:
            self.turn_label.config(text=f"{self.second}'s turn".capitalize())
        

    def __paint_tile(self, tile):
        symbol = 'X' if self.isMaxAgent else 'O'
        x = (tile % 3) * 200 + 100
        y = (tile // 3) * 200 + 100
        color = 'white' if symbol == 'X' else 'yellow'
        self.canvas.create_text(x, y, text=symbol, font=("Arial", 80),fill=color)

    @staticmethod
    def get_computer_move(player, computer, tiles):
        best_move = -1
        min_score = math.inf

        for move in tiles:
            new_computer = computer | {move}
            new_tiles = tiles - {move}
            score = Gamee.__minimax(player, new_computer, new_tiles, True)
            if score < min_score:
                min_score = score
                best_move = move

        return best_move

    @staticmethod
    def __minimax(max_agent, min_agent, tiles, is_max_agent):
        score = Gamee.__evaluate_win(max_agent, min_agent)
        if not tiles or score != 0:
            val = Gamee.__evaluate_win(max_agent, min_agent)
            return val

        if is_max_agent:
            max_val = -math.inf
            for move in tiles:
                new_agent = max_agent | {move}
                new_tiles = tiles - {move}
                val = Gamee.__minimax(new_agent, min_agent, new_tiles, False)
                max_val = max(max_val, val)
            return max_val
        else:  # min player
            min_val = math.inf
            for move in tiles:
                new_agent = min_agent | {move}
                new_tiles = tiles - {move}
                val = Gamee.__minimax(max_agent, new_agent, new_tiles, True)
                min_val = min(min_val, val)
            return min_val

    @staticmethod
    def __evaluate(max_player, min_player, available, is_max_player):
        bonus = len(available)
        score = Gamee.__evaluate_win(max_player, min_player)
        if score != 0:
            score = (score * bonus) + len(max_player) - len(min_player)

        return score

    # ------------------------------------------------------------------------
    #  Static Helper Functions: Evaluating Win or Draw
    # ------------------------------------------------------------------------
    @staticmethod
    def __evaluate_win(max_player, min_player):
        for win in Gamee.WINNING_STATES:
            if set(win).issubset(max_player):
                return 10
            elif set(win).issubset(min_player):
                return -10
        return 0

def play_sound(sound_file):
    music_file = os.path.join(os.getcwd(), sound_file)
    pygame.mixer.init()
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()

   


