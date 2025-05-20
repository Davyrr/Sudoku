import tkinter as tk
from tkinter import messagebox
import random
from sudokus import puzzleseasy, puzzlesmedium, puzzleshard

class Sudoku:
    def __init__(self, master):
        self.master = master
        self.master.title("Davud's Sudoku") # gives the game a title
        self.master.geometry("600x700")
        self.master.configure(bg="#f0f0f0")
        self.board = [[0 for _ in range(9)] for _ in range(9)] # creates a 9x9 empty sudoku board

        self.difficulty = tk.StringVar() # holds the difficulty level
        self.difficulty.set("Easy") # sets default difficulty to easy

        self.widgets() # add widgets function
        self.generate_board() # adds generate_board function

    def correctinput(self, val):
        if val == "":
            return True
        if len(val) == 1 and val in "123456789":
            return True # only digits from 1 to 9
        return False

    def widgets(self):
        menu = tk.Menu(self.master) # creates a menu bar
        self.master.config(menu=menu) # ensures that the menu bar is attached to the main window.

        difficulty_menu = tk.Menu(menu, tearoff=0) # creates a dropdown menu for difficulty levels
        menu.add_cascade(label="Difficulty", menu=difficulty_menu) # adds the dropdown menu to the menu bar
        difficulty_menu.add_radiobutton(label="Easy", variable=self.difficulty, value="Easy", command=self.generate_board)  # easy difficulty
        difficulty_menu.add_radiobutton(label="Medium", variable=self.difficulty, value="Medium", command=self.generate_board)  # medium difficulty
        difficulty_menu.add_radiobutton(label="Hard", variable=self.difficulty, value="Hard", command=self.generate_board)  # hard difficulty

        grid_frame = tk.Frame(self.master, bg="#000000", bd=2) # frame - border
        grid_frame.pack(pady=20)
        self.entries = [[None for _ in range(9)] for _ in range(9)] # creates a 9x9 matrix to store entry widgets for the sudoku grid

        correctdig = (self.master.register(self.correctinput), '%P') # only one digit

        for box_row in range(3):
            for box_col in range(3):
                sub_grid = tk.Frame(grid_frame, bg="#000000", bd=1) # border for 3x3 grids
                sub_grid.grid(row=box_row, column=box_col, padx=1, pady=1) # creates the 3x3 sub_grids in the main 9x9 Sudoku board
                for i in range(3):  
                    for j in range(3):
                        row = box_row * 3 + i # finding the positions of a cell in the full 9x9 grid
                        col = box_col * 3 + j # finding the column positions of a cell in the full 9x9 grid
                        entry = tk.Entry(
                            sub_grid,
                            width=2,
                            font=('Arial', 20),
                            justify='center',
                            bg="white",
                            validate="key",
                            validatecommand=correctdig # validates digits
                        )
                        entry.grid(row=i, column=j, padx=3, pady=3, ipadx=10, ipady=5)  # places the entry widget inside the corresponding 3x3 sub_grid
                        self.entries[row][col] = entry # storing the entry widget

        btn_check = tk.Button( # button decoration
            self.master,
            text="Check Solution",
            command=self.check_solution,
            font=("Arial", 14, "bold"),
            bg="#007BFF",
            fg="white",
            relief="raised",
            bd=3,
            padx=20,
            pady=10,
        )
        btn_check.pack(pady=20)

    def generate_board(self):
        difficulty = self.difficulty.get()
        if difficulty == "Easy":
            puzzles = puzzleseasy # set difficulty to easy
        elif difficulty == "Medium":
            puzzles = puzzlesmedium # set difficulty to medium
        elif difficulty == "Hard":
            puzzles = puzzleshard # set difficulty to hard
        else:
            puzzles = puzzleseasy

        puzzle_number = random.choice(list(puzzles.keys())) # chooses one of the sudokus
        self.board = [row[:] for row in puzzles[puzzle_number]]
        for i in range(9):
            for j in range(9):
                self.entries[i][j].config(state='normal', bg="white") # makes all cells editable before filling the board with sudoku templates
                if self.board[i][j] != 0: # if the cell has a number
                    self.entries[i][j].delete(0, tk.END) # clears any existing value
                    self.entries[i][j].insert(0, str(self.board[i][j])) # adds the number from the board
                    self.entries[i][j].config(state='readonly') # makes the cell read-only
                else:
                    self.entries[i][j].delete(0, tk.END) # clears the cell for input

    def check_solution(self):
        user_board = [[0 for _ in range(9)] for _ in range(9)] # creating a 9x9 board to store the user's inputs

        for i in range(9):  
            for j in range(9):
                val = self.entries[i][j].get() # getting the value entered by the user in the cell
                user_board[i][j] = int(val) if val.isdigit() else 0 # change the value to an integer if it is a digit, if not, set it to 0
                self.entries[i][j].config(bg="white") # setting the background color of the cell to white, better visuals

        incorrect = False
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0 and not self.is_cell_valid(user_board, i, j): # if user input is incorrect
                    self.entries[i][j].config(bg="red") # highlights incorrect cells in red
                    incorrect = True

        if incorrect: # if incorrect,
            messagebox.showerror("Sudoku", "The solution is incorrect. Try again.") # show this message 
        elif any(0 in row for row in user_board): # if there are still empty cells,
            messagebox.showerror("Sudoku", "The board is not completely filled. Please complete it.") # show this message
        else: # if the solution is correct,
            messagebox.showinfo("Sudoku", "Congratulations! You solved the Sudoku!") # show this message

    def is_cell_valid(self, board, row, col):
        value = board[row][col] # getting the value of the current cell
        if value == 0: # if the cell is empty,
            return True # it is valid
        if board[row].count(value) > 1: # checking if the value appears multiple times in the row
            return False
        if [board[r][col] for r in range(9)].count(value) > 1: # checking if the value appears multiple times in the column
            return False
        box_row, box_col = (row // 3) * 3, (col // 3) * 3 # finding the 3x3 grid
        box = [board[r][c] for r in range(box_row, box_row + 3) for c in range(box_col, box_col + 3)] # storing all values in 3x3 grids
        return box.count(value) <= 1 # ensures unique values

if __name__ == "__main__":
    root = tk.Tk()
    game = Sudoku(root)
    root.mainloop()
