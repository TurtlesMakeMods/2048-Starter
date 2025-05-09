"""
Project: "2048 in Python!"

Developed by: Kunal Mishra and Paradigm Shift
Autograder support, video introductions added by: Jesse Luo and Michael Tu

Developed for: Beginning students in Computer Science

To run: python3 starter_2048.py

Student Learning Outcomes:
    Various levels of comfort with:
        large projects and abstraction
        understanding, modeling, and maintaining existing code
        variables
        functional programming
        loops and conditionals
        multidimensional arrays/lists
        randomness and distributions
        CLI programming and terminal GUIs

Skill Level:
    assumed knowledge of language and concepts, but without mastery or even comfortability with them
    ~8-15 hours of lecture/lab/homework for a beginner at CS0 level coming into this project
    ~Calibrated at somewhat below the difficulty level of UC Berkeley's 61A project, Hog (less code synthesis but more interpretation required, given the students' backgrounds) 

Abstraction Reference Guide:

    main                - responsible for starting the game and directing control to each function, the tests, or quitting
        board           - a variable within main that contains the current board and is passed to most functions as an argument

    System Functions:
        get_key_press   - returns the user's key_press input as an ascii value
        clear           - clears the screen (should be called before each print_board call)
        pause           - a function used by the GUI to allow for a slight delay that is more visually appealing in placing the new piece


    Board Functions:
        make_board      - creates a new, empty square board of N x N dimension
        print_board     - prints out the state of the argument board
        board_full      - returns True if the board is full and False otherwise


    Logic:
        swipe_right     - simulates a right swipe on the argument board
        swipe_left      - simulates a left swipe on the argument board
        swipe_up        - simulates a upward swipe on the argument board
        swipe_down      - simulates a downward swipe on the argument board
        swap            - occurs when the spacebar is pressed and randomly switches two different numbers on the board
        swap_possible   - a helper function that returns True if a swap is possible and False otherwise


    Useful Helper Functions:
        get_piece       - gets the piece from the given board at the given (x,y) coordinates or returns None if the position is invalid
        place_piece     - places the given piece on the given board at the given (x,y) coordinates and returns True or returns False if the position is invalid
        place_random    - user implemented function which places a random 2 OR 4 OR 8 in an empty part of the board
        have_lost       - responsible for determining if the game has been lost yet (no moves remain)
        move_possible   - responsible for determining if a move is possible from a single position
        move            - responsible for moving a piece, at the given (x,y) coordinates in the given direction on the given board

"""

#End of first section
############################################################################################################
################################## DO NOT CHANGE ANYTHING ABOVE THIS LINE ##################################    - Section 2 -
############################################################################################################

import random

def main():
    # Creating my new 4x4 board
    board = make_board(4)

    # Getting the game started with a single piece on the board
    place_random(board)

    # Runs the game loop until the user quits or the game is lost
    while True:
        # Print the board after each move
        print_board(board)

        # Gets the key pressed and stores it in the key variable
        key = input("Enter move (w=up, s=down, a=left, d=right, q=quit, space=swap): ").strip()

        # Quit case ('q')
        if key == 'q':
            print("Game Finished!")
            quit()

        # Up arrow
        elif key == 'w':
            swipe_up(board)

        # Down arrow
        elif key == 's':
            swipe_down(board)

        # Right arrow
        elif key == 'd':
            swipe_right(board)

        # Left arrow
        elif key == 'a':
            swipe_left(board)

        # Space bar
        elif key == ' ':
            swap(board)

        # Check to see if I've lost at the end of the game or not
        if have_lost(board):
            print("You lost! Would you like to play again? (y/n)")
            if input().strip().lower() == 'y':
                main()
            else:
                quit()

def make_board(size):
    """
    Creates a size x size board filled with '*'
    """
    return [['*' for _ in range(size)] for _ in range(size)]

def print_board(board):
    """
    Prints the current state of the board
    """
    print("\nCurrent board:")
    for row in board:
        print(" ".join(row))
    print()

def get_piece(x, y, board):
    """
    Gets the piece at (x, y) if valid, else returns None
    """
    N = len(board)
    if 0 <= x < N and 0 <= y < N:
        return board[y][x]
    return None

def place_piece(piece, x, y, board):
    """
    Places a piece at (x, y) if valid
    """
    N = len(board)
    if 0 <= x < N and 0 <= y < N:
        board[y][x] = piece
        return True
    return False

def place_random(board):
    """
    Places a 2 (60%), 4 (37%), or 8 (3%) on a random empty spot
    """
    empty = [(y, x) for y in range(len(board)) for x in range(len(board)) if board[y][x] == '*']
    if not empty:
        return False

    y, x = random.choice(empty)

    rnd = random.random() * 100
    if rnd < 60:
        piece = '2'
    elif rnd < 97:
        piece = '4'
    else:
        piece = '8'

    board[y][x] = piece
    return True

def have_lost(board):
    """
    Checks if there are no moves left
    """
    if any('*' in row for row in board):
        return False

    N = len(board)
    for y in range(N):
        for x in range(N):
            if move_possible(x, y, board):
                return False
    return True

def move_possible(x, y, board):
    """
    Checks if a move is possible at (x, y)
    """
    piece = get_piece(x, y, board)
    if piece == '*':
        return True

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        neighbor = get_piece(x + dx, y + dy, board)
        if neighbor == piece:
            return True
    return False

def swipe_left(board):
    """
    Swipes the board left
    """
    moved = False
    for row in board:
        new_row = [num for num in row if num != '*']
        i = 0
        while i < len(new_row) - 1:
            if new_row[i] == new_row[i + 1]:
                new_row[i] = str(int(new_row[i]) * 2)
                del new_row[i + 1]
                moved = True
            i += 1
        new_row += ['*'] * (len(board) - len(new_row))
        if row != new_row:
            moved = True
        row[:] = new_row
    if moved:
        place_random(board)

def swipe_right(board):
    """
    Swipes the board right
    """
    for row in board:
        row.reverse()
    swipe_left(board)
    for row in board:
        row.reverse()

def swipe_up(board):
    """
    Swipes the board up
    """
    transpose(board)
    swipe_left(board)
    transpose(board)

def swipe_down(board):
    """
    Swipes the board down
    """
    transpose(board)
    swipe_right(board)
    transpose(board)


def transpose(board):
    """
    Transposes the board in place
    """
    N = len(board)
    for y in range(N):
        for x in range(y + 1, N):
            board[y][x], board[x][y] = board[x][y], board[y][x]

def swap(board):
    """
    Swaps the first and last rows (example swap function)
    """
    board[0], board[-1] = board[-1], board[0]

if __name__ == '__main__':
    main()