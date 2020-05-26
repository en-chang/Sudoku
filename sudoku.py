import requests
import json
import pprint

# Calls a sudoku API to generate a sudoku board based on a difficulty level
# Source: "http://www.cs.utep.edu/cheon/ws/sudoku/"
def createBoard(difficulty):
    response = requests.get(f"http://www.cs.utep.edu/cheon/ws/sudoku/new/?size=9&level={difficulty}")
    data = response.json()
    data = data['squares']
    board = [[0] * 9 for row in range(9)]
    for point in range(len(data)):
        col = data[point]['x']
        row = data[point]['y']
        val = data[point]['value']
        board[row][col] = val
    return board

# Solves sudoku boards using backtracking
def sudokuSolver(board, row, col):
    if sudokuComplete(board) is True:
        global completeBoard
        completeBoard = board
        return True
    if board[row][col] == 0:
        # Find nums that are potential guesses in a row
        usedNums = [num for num in board[row] if num in range(1, 10)]
        possibNums = [num for num in range(1, 10) if num not in usedNums]
        for guess in possibNums:
            board[row][col] = guess
            # Print statements to show the process
            '''
            print('row, col', (row, col))
            print('guess', guess)
            printBoard(board)
            print()
            '''
            if sudokuChecker(board) is True:
                if rowComplete(board[row]) is True:
                    if sudokuSolver(board, row + 1, 0) is True:
                        return True
                elif sudokuSolver(board, row, col + 1) is True:                    
                    return True
                board[row][col] = 0
                continue
            # Backtrack if all guesses are wrong
            if guess == possibNums[-1]:
                board[row][col] = 0
                return False
        # Backtracking multiple steps
        if board[row][col] == 0:
            return False
    # Continue to next col if space is filled
    if sudokuSolver(board, row, col + 1) is True:
        return True

# Checks if the board is valid
def sudokuChecker(board):
    if rowChecker(board) is False:
        return False
    if colChecker(board) is False:
        return False
    if subSquareChecker(board) is False:
        return False
    return True

# Helper function to sudokuChecker and sudokuComplete
def rowChecker(board):
    # Check rows for duplicates except 0 (empty spaces)
    for i in range(len(board)):
        # Remove 0s
        row = [x for x in board[i] if x != 0]
        if dupChecker(row) is False:
            return False

# Helper function to sudokuChecker
def colChecker(board):
    # Check columns for duplicates except 0
    for i in range(len(board)):
        col = []
        for j in range(len(board[i])):
            col.append(board[j][i])
        # Remove 0s
        col = [x for x in col if x != 0]
        if dupChecker(col) is False:
            return False

# Helper function to sudokuChecker
def subSquareChecker(board):
    # Loop within the first, fourth, and seventh row 3 times
    # Because this is the start of the subSquares
    for i in range(0, len(board), 3):
        subSquare = []
        # Check two rows ahead to form subSquare
        # Because this finishes the subSquares
        # After each subSquare check with dupChecker
        for j in range(0, len(board[i]), 3):
            subSquare.extend(board[i][j : j + 3])
            subSquare.extend(board[i + 1][j : j + 3])
            subSquare.extend(board[i + 2][j : j + 3])
            # Remove 0s
            subSquare = [x for x in subSquare if x != 0]
            if dupChecker(subSquare) is False:
                return False
            subSquare.clear()
    return True

# Helper function to row/col/subSquareChecker
# Checks for duplicates in a row, col, or subSquare
def dupChecker(rowOrCol):
    if len(rowOrCol) != len(set(rowOrCol)):
        return False
    ''' # For testing purposes
    else:
        print(rowOrCol)
        print('correct row, col, or subSquare')
    '''

# Helper function to sudokuSolver
def sudokuComplete(board):
    for i in range(len(board)):
        if rowComplete(board[i]) is False:
            return False
    return True

# Heper function to sudokuComplete
def rowComplete(row):
    if 0 in row:
        return False
    return True

def printBoard(board):
    boardPrinter = pprint.PrettyPrinter()
    boardPrinter.pprint(board)

# Sample board for testing
'''
testBoard = [
    [4, 0, 0, 0, 0, 0, 1, 0, 7],
    [2, 1, 0, 5, 0, 7, 0, 9, 0],
    [7, 0, 3, 0, 0, 0, 2, 0, 4],
    [0, 0, 0, 3, 1, 0, 0, 0, 9],
    [6, 0, 0, 0, 5, 0, 0, 0, 0],
    [5, 3, 1, 0, 0, 9, 0, 0, 0],
    [0, 7, 0, 1, 0, 0, 0, 2, 8],
    [0, 0, 0, 0, 0, 4, 0, 6, 3],
    [0, 6, 0, 0, 0, 0, 0, 0, 0]
    ]
'''

def main():
    easy = 1
    medium = 2
    hard = 3
    board = createBoard(medium)
    print('Board:')
    printBoard(board)
    print()
    global completeBoard
    sudokuSolver(board, 0, 0)
    print('Solution:')
    printBoard(completeBoard)

if __name__ == "__main__":
    main()
