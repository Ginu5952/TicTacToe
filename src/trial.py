import tkinter
from tkinter import messagebox
import math


class Game(object):
    WINNING_STATES = ((0, 1, 2), (3, 4, 5), (6, 7, 8),  # row
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),  # column
                      (0, 4, 8), (2, 4, 6))  # diagonal

    def __init__(self, parent, player_names):
        self.players = {name: set() for name in player_names}
        self.current_player_index = 0  # Index of the current player in the player_names list

        parent.title('Tic Tac Toe')
        parent.configure(bg='white')  # Set background color
        parent.option_add('*Font', 'Helvetica 18 bold')
        canvas = tkinter.Canvas(parent, width=600, height=600, bg='lightblue')
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

        result_string = tkinter.StringVar()
        tkinter.Label(parent, height=2, textvariable=result_string).grid()

        self.result = result_string
        self.canvas = canvas
        self.filled = set()
        self.tiles = set(range(9))
        self.maxAgent = set()
        self.minAgent = set()
        self.isMaxAgent = True

    def restart(self):
        for filled_tile in self.canvas.find_all():
            self.canvas.itemconfigure(filled_tile, fill='')

        self.result.set('')
        self.filled = set()
        self.tiles = set(range(9))
        self.maxAgent = set()
        self.minAgent = set()
        self.isMaxAgent = True


    def play(self, event):
        current_player_name = list(self.players.keys())[self.current_player_index]
        current_player_tiles = self.players[current_player_name]

        # Check if it's the turn of the second player
        if current_player_name == 'Player2':
            # Manually mark the tile
            tile = (event.y // 200) * 3 + (event.x // 200)
            if tile not in current_player_tiles and tile in self.tiles:
                self.__update_board_canvas(tile)
                self.__update_game_state(tile, current_player_name)
                self.__update_result_label()
                self.current_player_index = (self.current_player_index + 1) % len(self.players)
        else:
            # Allow the first player to play as before
            score = Game.__evaluate_win(self.maxAgent, self.minAgent)
            if score == 0 and self.tiles and self.isMaxAgent:
                tile = (event.y // 200) * 3 + (event.x // 200)
                self.__update_board_canvas(tile)
                self.__update_game_state(tile, current_player_name)
                self.__update_result_label()
                self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def __update_game_state(self, tile, current_player_name):
        try:
            self.tiles.remove(tile)
            self.players[current_player_name].add(tile)
            self.isMaxAgent = not self.isMaxAgent
        except KeyError as key_error:
            pass

    def __update_board_canvas(self, tile):
        if tile not in self.maxAgent and tile not in self.minAgent:
            self.__paint_tile(tile)

    def __update_result_label(self):
        score = Game.__evaluate_win(self.maxAgent, self.minAgent)
        if score == 10:
            messagebox.showinfo("Game Over", f"{list(self.players.keys())[0]} You Win!")
        elif score == -10:
            messagebox.showinfo("Game Over", f"{list(self.players.keys())[1]} Wins!")
        elif score == 0 and len(self.tiles) == 0:
            messagebox.showinfo("Game Over", "Draw")

    

    def __paint_tile(self, tile):
        symbol = 'X' if self.isMaxAgent else 'O'
        color = 'white' if self.isMaxAgent else 'yellow'
        x = (tile % 3) * 200 + 100
        y = (tile // 3) * 200 + 100
        self.canvas.create_text(x, y, text=symbol, font=("Arial", 80), fill=color)

    @staticmethod
    def __evaluate_win(max_player, min_player):
        for win in Game.WINNING_STATES:
            if set(win).issubset(max_player):
                return 10
            elif set(win).issubset(min_player):
                return -10
        return 0


if __name__ == "__main__":
    root = tkinter.Tk()
    game = Game(root, ["Player1", "Player2"])
    root.mainloop()
