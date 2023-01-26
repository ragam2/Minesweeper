import tkinter.messagebox
from tkinter import *
import random
import os

# Used for event bindings
left_click = "<Button-1>"
# right click can be button 2 or 3 for some reason, with the additional
# button being the mouse wheel usually
right_click_2 = "<Button-2>"
right_click_3 = "<Button-3>"

# File path to grab photos
dir_path = os.path.dirname(os.path.realpath(__file__))


class Minesweeper:
    def __init__(self, tk, board_size, total_mines):
        # Start menu window
        self.tk = tk

        # Contains images used in minesweeper games.
        self.images = {
            0: PhotoImage(file=dir_path + "/0.png"),
            1: PhotoImage(file=dir_path + "/1.png"),
            2: PhotoImage(file=dir_path + "/2.png"),
            3: PhotoImage(file=dir_path + "/3.png"),
            4: PhotoImage(file=dir_path + "/4.png"),
            5: PhotoImage(file=dir_path + "/5.png"),
            6: PhotoImage(file=dir_path + "/6.png"),
            7: PhotoImage(file=dir_path + "/7.png"),
            8: PhotoImage(file=dir_path + "/8.png"),
            "facing down": PhotoImage(file=dir_path + "/facingDown.png"),
            "bomb": PhotoImage(file=dir_path + "/bomb.png"),
            "flagged": PhotoImage(file=dir_path + "/flagged.png"),
        }

        # Sets the score to 0, and gets the board size & total mines (difficulty)
        self.score = 0
        self.board_size = board_size
        self.total_mines = total_mines

        # Create data & run game window
        self.generate_board()
        self.game_window()

    def generate_board(self):
        # initialize board dimensions (row x cols) & total mines
        rows = self.board_size
        cols = self.board_size

        # Create a 2D list with the dimensions rows x cols
        # Cell is a dictionary containing xy coordinates, booleans for tile states, tile value, and button
        # Create cell board
        self.cell_board = [
            [{
                "coordinates": None,
                "is_mine": False,
                "is_flagged": False,
                "is_revealed": False,
                "value": 0,
                "button": None,
            } for i in range(0, rows)] for j in range(0, cols)]

        current_mine_amount = 0  # Counter to compare with total mines, for the while loop
        while current_mine_amount != self.total_mines:
            if current_mine_amount == self.total_mines:
                continue
            # Generate a random x,y coordinate for the mine to be placed, subtract 1 to match index
            x = random.randint(0, rows - 1)
            y = random.randint(0, cols - 1)

            # Mines denoted by M
            # Avoid duplicate mines
            if self.cell_board[x][y]["value"] == "M":
                continue
            else:
                self.cell_board[x][y]["value"] = "M"
                self.cell_board[x][y]["is_mine"] = True
                self.cell_board[x][y]["coordinates"] = (x, y)
                current_mine_amount += 1

            # Get the adjacent tile coordinates
            neighbors = {
                "top left": {"x": x - 1, "y": y - 1},
                "center left": {"x": x, "y": y - 1},
                "bottom left": {"x": x + 1, "y": y - 1},
                "top right": {"x": x - 1, "y": y + 1},
                "center right": {"x": x, "y": y + 1},
                "bottom right": {"x": x + 1, "y": y + 1},
                "up": {"x": x - 1, "y": y},
                "down": {"x": x + 1, "y": y}
            }

            # Update values surrounding the cell, while accounting for edge cases
            if neighbors["top left"]["x"] >= 0 and neighbors["top left"]["y"] >= 0:
                if self.cell_board[x - 1][y - 1]["value"] != "M":
                    self.cell_board[x - 1][y - 1]["value"] += 1

            if neighbors["center left"]["y"] >= 0:
                if self.cell_board[x][y - 1]["value"] != "M":
                    self.cell_board[x][y - 1]["value"] += 1

            if neighbors["bottom left"]["x"] <= rows - 1 and neighbors["bottom left"]["y"] >= 0:
                if self.cell_board[x + 1][y - 1]["value"] != "M":
                    self.cell_board[x + 1][y - 1]["value"] += 1

            if neighbors["top right"]["x"] >= 0 and neighbors["top right"]["y"] <= cols - 1:
                if self.cell_board[x - 1][y + 1]["value"] != "M":
                    self.cell_board[x - 1][y + 1]["value"] += 1

            if neighbors["center right"]["y"] <= cols - 1:
                if self.cell_board[x][y + 1]["value"] != "M":
                    self.cell_board[x][y + 1]["value"] += 1

            if neighbors["bottom right"]["x"] <= rows - 1 and neighbors["bottom right"]["y"] <= cols - 1:
                if self.cell_board[x + 1][y + 1]["value"] != "M":
                    self.cell_board[x + 1][y + 1]["value"] += 1

            if neighbors["up"]["x"] >= 0:
                if self.cell_board[x - 1][y]["value"] != "M":
                    self.cell_board[x - 1][y]["value"] += 1

            if neighbors["down"]["x"] <= rows - 1:
                if self.cell_board[x + 1][y]["value"] != "M":
                    self.cell_board[x + 1][y]["value"] += 1

        # Print table, for debugging
        # print("\nCell Board")
        # self.print_cell_board()

    def print_cell_board(self):
        # brute force printing the cell values, for debugging purposes
        for i in self.cell_board:
            string = ""
            for j in i:
                string += (str(j["value"]) + " ")
            print(string + "\n")

    def game_window(self):

        # Title for the window
        self.tk.title("Minesweeper - Game")

        # Creates frame for the label depicting uncovered mines.
        label_frame = Frame(self.tk, width=100, height="300")
        label_frame.pack(side="top")

        #self.save_and_exit = Button(label_frame, text="Save and Exit")
        #self.save_and_exit.pack(side="left")

        self.score_label = Label(label_frame, text="Score: " + str(self.score), width=50)
        self.score_label.pack(side="right")

        # Creates buttons for the game
        button_frame = Frame(self.tk, width=100)
        button_frame.pack(side="top")

        # Updates cell board with appropriate buttons to display when clicked
        for x in range(self.board_size):
            for y in range(self.board_size):
                self.cell_board[x][y]["button"] = Button(
                    button_frame,
                    image=self.images["facing down"],
                    height=50,
                    width=50,
                )
                # Creates click events for right and left, and assigns them to proper functions
                self.cell_board[x][y]["button"].bind(left_click, self.left_click_event((x, y)))
                self.cell_board[x][y]["button"].bind(right_click_2, self.right_click_event((x, y)))
                self.cell_board[x][y]["button"].bind(right_click_3, self.right_click_event((x, y)))
                self.cell_board[x][y]["button"].grid(row=x, column=y)

        mainloop()

    def reveal_adjacent_tiles(self, coord, coord_dct):
        # coord_dct is used to speed up program by keeping track of visited indexes
        x = coord[0]
        y = coord[1]
        try:
            if coord_dct[(x, y)] == "Visited":
                return 0
        except KeyError:
            coord_dct[(x, y)] = "Visited"

        neighbors = {
            "center left": {"x": x, "y": y - 1},
            "center right": {"x": x, "y": y + 1},
            "up": {"x": x - 1, "y": y},
            "down": {"x": x + 1, "y": y}
        }
        for item in neighbors:
            # Handles index errors by continuing the loop
            try:
                # Assign values from neighbors dictionary
                temp_x = neighbors[item]["x"]
                temp_y = neighbors[item]["y"]
                # Prevents a -1, which would lead to incorrect cells being uncovered at the end of the
                # cell_board list
                if temp_x < 0:
                    temp_x = 0
                if temp_y < 0:
                    temp_y = 0

                cell = self.cell_board[temp_x][temp_y]

                # 0 Cells have their command removed, image changed,
                # and their neighbors checked
                if cell["value"] == 0:
                    cell["is_revealed"] = True
                    cell["button"].config(image=self.images[0])
                    cell["button"].config(command=None)
                    self.reveal_adjacent_tiles((temp_x, temp_y), coord_dct)
            except IndexError:
                coord_dct[(temp_x, temp_y)] = "Visited"
                continue
            coord_dct[(temp_x, temp_y)] = "Visited"

        # update score & score label
        self.score += 1
        self.score_label.config(text="Score: " + str(self.score))
        self.tk.update()

    def left_click_event(self, coord):
        # this is needed for some reason, it works so i aint asking questions
        return lambda button: self.when_left_clicked(coord)

    def when_left_clicked(self, coord):
        x = coord[0]
        y = coord[1]
        cell = self.cell_board[x][y]
        cell_value = self.cell_board[x][y]["value"]
        if cell["is_mine"]:
            cell["is_revealed"] = True
            cell["button"].config(image=self.images["bomb"])
            cell["button"].config(command=None)
            self.game_over()
            return
        elif cell["value"] == 0:
            if cell["is_revealed"]:
                return
            else:
                cell["is_revealed"] = True
                cell["button"].config(image=self.images[cell_value])
                cell["button"].config(command=None)
                self.reveal_adjacent_tiles(coord, {})
                self.check_score()
        else:
            if cell["is_revealed"]:
                return
            else:
                cell["is_revealed"] = True
                cell["button"].config(image=self.images[cell_value])
                cell["button"].config(command=None)
                self.score += 1
                self.score_label.config(text="Score: " + str(self.score))
                self.check_score()

        self.tk.update()

    def right_click_event(self, coord):
        # This function is needed, but I can't articulate why.
        return lambda button: self.when_right_clicked(coord)

    def when_right_clicked(self, coord):
        # get x & y coordinates
        x = coord[0]
        y = coord[1]
        cell = self.cell_board[x][y]  # create cell

        # changes image on the button depending on if its flagged & revealed
        if cell["is_flagged"]:
            cell["button"].config(image=self.images["facing down"])
            cell["is_flagged"] = False
        else:
            if not cell["is_revealed"]:
                cell["button"].config(image=self.images["flagged"])
                cell["is_flagged"] = True
        self.tk.update()

    def game_over(self):
        # Create a window prompt informing them they lost, and
        # prompts the user if they'd like to play again.
        game_over_screen = tkinter.messagebox.askyesno(
            "Game Over!",
            message="You lost! Would you like to return to the start menu?"
        )

        if game_over_screen:
            self.tk.destroy()
            start_menu()

        else:
            self.tk.destroy()

    def check_score(self):
        # Checks if the victory condition has been met,
        # which is if all spaces have been uncovered
        # score should equal (board size * board size) - total mines
        if self.score == (self.board_size * self.board_size) - self.total_mines:
            victory_screen = tkinter.messagebox.askyesno(
                "Victory!",
                message="You won! Would you like to play again?"
            )
            if victory_screen:
                self.tk.destroy()
                start_menu()
            else:
                self.tk.destroy()


def start_menu():
    # Create the start window, modify size & title
    start_window = Tk()
    start_window.geometry("300x515")
    start_window.title("Minesweeper")

    # Create the welcome message
    welcome = Label(text="Welcome to Minesweeper!\n "
                         "Select a difficulty to begin!")
    welcome.pack(side="top")

    # Create frame that holds difficulty selection buttons
    button_frame = Frame(start_window)

    # Create buttons. Each button has a destroy() function to
    # close out the start menu after clicking

    # 8x8, 1 Mine, pretty much to test if the victory screen works
    super_easy_button = Button(button_frame, text="Super Easy (8x8)",
                               height=5,
                               width=15,
                               command=lambda: [start_window.destroy(),
                                                Minesweeper(Tk(), 8, 1)])
    super_easy_button.pack(side="top")

    # 8x8, 4 Mines
    easy_button = Button(button_frame, text="Easy (8x8)",
                         height=4,
                         width=15,
                         command=lambda: [start_window.destroy(),
                                          Minesweeper(Tk(), 8, 3)])
    easy_button.pack(side="top")

    # 10x10 10 Mines
    medium_button = Button(button_frame, text="Medium (10x10)",
                           height=4,
                           width=15,
                           command=lambda: [start_window.destroy(),
                                            Minesweeper(Tk(), 10, 10)])
    medium_button.pack(side="top")

    # 15x15, 20 Mines
    hard_button = Button(button_frame, text="Hard (15x15)",
                         height=4,
                         width=15,
                         command=lambda: [start_window.destroy(),
                                          Minesweeper(Tk(), 15, 20)])
    hard_button.pack(side="top")

    help_button = Button(button_frame, text="Help",
                         height=3,
                         width=15,
                         bg="dodger blue",
                         command=help_window)
    help_button.pack(side="bottom")
    button_frame.pack(side="top")

    # My name to the bottom.
    team = Label(text="Rahman Gamble")
    team.pack(side="bottom")

    mainloop()


def help_window():
    # Prints instructions when pressed on the main menu
    window = tkinter.messagebox.showinfo(
        title="Minesweeper - Help",
        message="The board consists of x by x tiles. ("
                "8x8 on Super Easy and Easy, 10x10 on Medium,"
                " 15x15 on Hard)\n\n"
                "When clicking a tile, you either reveal a "
                "blank space, a number, or a mine.\n\n"
                "If a blank space is revealed, all adjacent blank spaces "
                "will also be revealed (including diagonals).\n\n"
                "If a number is revealed, that number represents the amount of"
                " mines adjacent to the tile (including diagonals).\n\n"
                "If you reveal a mine, you lose.\n\n"
                "The player must guess which tiles are safe to reveal, until no"
                " safe tiles remain.\n\n"
                "The player also can right-click on tiles to place a “flag” on"
                " them, to help them keep track of potential mines."
    )

    mainloop()


def main():
    start_menu()


main()
