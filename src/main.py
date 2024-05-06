from . import board
from src.tictactoe import Game
import tkinter
from src.multiplePlayer import Gamee
import os

def menu() -> str:
   while True:
        print("Menu:")
        print("1) Play with computer")
        print("2) Play with second player")
        print("3) Quit")
        choice = input("Enter your choice: ")

        if choice in {"1", "2", "3"}:
            return choice
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def clear_screen():
        # Clear the terminal screen
        os.system('cls' if os.name == 'nt' else 'clear')             

def main():
    clear_screen()
    print('\n')
    board.welcome_message()
    print('\n')
    player_one:str=board.player_give_your_name(1)
    print('\n')
    choose = menu()
    print('\n')

    if choose == '1':
        computer = {0,7,5}
        player = {1,2,3,4}
        available = {6,8}
    
        root = tkinter.Tk()
    
        game = Game(root,player_one.capitalize())
    
        root.mainloop()
    elif choose == '2':    
        
        player_two:str=board.player_give_your_name(2)
        
        root = tkinter.Tk()
        
        game = Gamee(root,player_one,player_two)
      
        root.mainloop()

if __name__=="__main__":
    main()


    
