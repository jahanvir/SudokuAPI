from flask import Flask, request, jsonify

app = Flask(__name__)

# Global variable to store the Sudoku board
board = [[0] * 9 for _ in range(9)]
skeleton = [[0] * 9 for _ in range(9)]
# Helper function to check if a move is valid
def is_valid_move(row, col, value):
    # Check if the value is already present in the row
    if value in board[row]:
        return False

    # Check if the value is already present in the column
    for i in range(9):
        if board[i][col] == value:
            return False

    # Check if the value is already present in the 3x3 sub-grid
    subgrid_row = (row // 3) * 3
    subgrid_col = (col // 3) * 3
    for i in range(subgrid_row, subgrid_row + 3):
        for j in range(subgrid_col, subgrid_col + 3):
            if board[i][j] == value:
                return False

    # If none of the checks failed, the move is valid
    return True

# Reset the Sudoku board
def reset_board():
    global board
    board = [[0] * 9 for _ in range(9)]

@app.route('/start', methods=['GET'])
def start():
    reset_board()
    return jsonify(message='Sudoku board has been reset. Ready to play.')

@app.route('/add_sudoku', methods=['POST'])
def add_sudoku():
    sudoku = request.json.get('sudoku')

    if sudoku is None:
        return jsonify(message='Sudoku not provided.')

    if len(sudoku) != 9:
        return jsonify(message='Invalid Sudoku. The board must have 9 rows.')

    for row in sudoku:
        if len(row) != 9:
            return jsonify(message='Invalid Sudoku. Each row must have 9 columns.')

    # Assign the Sudoku values to the board
    global board
    board = sudoku
    global skeleton
    skeleton=sudoku

    return jsonify(message='Sudoku skeleton added successfully.')

@app.route('/move', methods=['POST'])
def move():
    print("request is ", request.form)
    row = int(request.form.get('row'))
    col = int(request.form.get('column'))
    value = int(request.form.get('value'))

    if skeleton[row][col] != 0:
        return jsonify(message='Cannot modify initial Sudoku skeleton.')
    
    if is_valid_move(row, col, value):
        board[row][col] = value
        return jsonify(message='Valid move.')
    else:
        return jsonify(message='Invalid move.')

if __name__ == '__main__':
    app.run()
