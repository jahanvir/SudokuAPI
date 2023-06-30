from flask import Flask, request, jsonify
app = Flask(__name__)

# Global variable to store the Sudoku board
board = [[0] * 9 for _ in range(9)]
skeleton = [[0] * 9 for _ in range(9)]
# Global variable to keep track of consecutive wrong moves
consecutive_wrong_moves = 0

# Helper function to check if a move is valid
def is_valid_move(row, col, value):
    global skeleton
    # Check if the value is already present in the row
    if skeleton[row][col]:
        return False
    if value in board[row]:
        if not (board[row][col]==value):
            return False

    # Check if the value is already present in the column
    for i in range(9):
        if board[i][col] == value and i!=row:
            return False

    # Check if the value is already present in the 3x3 sub-grid
    subgrid_row = (row // 3) * 3
    subgrid_col = (col // 3) * 3
    for i in range(subgrid_row, subgrid_row + 3):
        for j in range(subgrid_col, subgrid_col + 3):
            if board[i][j] == value and i!=row and j!=col:
                return False

    # If none of the checks failed, the move is valid
    return True
# Helper function to check if the Sudoku is solved
def is_sudoku_solved():
    for row in board:
        if 0 in row:
            return False
    return True
# Reset the Sudoku board
def reset_board():
    global board, skeleton, consecutive_wrong_moves
    board.extend(skeleton)
    consecutive_wrong_moves=0

# Function to suggest a valid move
def suggest_move():
    global board
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for value in range(1, 10):
                    if is_valid_move(row, col, value):
                        return row, col, value
    return None

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
    global skeleton
    skeleton=sudoku
    reset_board()
   
    

    return jsonify(message='Sudoku skeleton added successfully.')

@app.route('/move', methods=['POST'])
def move():
    
    global consecutive_wrong_moves,skeleton
    row = int(request.form.get('row'))
    col = int(request.form.get('column'))
    value = int(request.form.get('value'))
    
    
    
    if is_valid_move(row, col, value):
        board[row][col] = value
        consecutive_wrong_moves=0
        if is_sudoku_solved():
            return jsonify(message='Valid move. Sudoku solved!')
        else:
            return jsonify(message='Valid move.')
    else:
        consecutive_wrong_moves += 1
        if consecutive_wrong_moves >= 3:
            suggested_move = suggest_move()
            if suggested_move is not None:
                suggested_row, suggested_col, suggested_value = suggested_move
                response = {
                    'message': 'Invalid move. Three consecutive wrong moves made. Suggested move:',
                    'suggested_row': suggested_row,
                    'suggested_col': suggested_col,
                    'suggested_value': suggested_value
                }
                return jsonify(response)
            else:
                return jsonify(message='Invalid move.')
        else:
            return jsonify(message='Invalid move.')
    
if __name__ == '__main__':
    app.run()
