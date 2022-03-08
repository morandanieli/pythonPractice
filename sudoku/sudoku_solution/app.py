from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)


def generate_board():
    # TODO generate a valid board
    board = [[5,3,".",".",7,".",".",".","."]
,[6,".",".",1,9,5,".",".","."]
,[".",9,8,".",".",".",".",6,"."]
,[8,".",".",".",6,".",".",".",3]
,[4,".",".",8,".",3,".",".",1]
,[7,".",".",".",2,".",".",".",6]
,[".",6,".",".",".",".",2,8,"."]
,[".",".",".",4,1,9,".",".",5]
,[".",".",".",".",8,".",".",7,9]]
    return board


def check_valid(board):
    res = validate(board)
    return {"result": res}


def findNextCellToFill(grid, i, j):
    for x in range(i, 9):
        for y in range(j, 9):
            if grid[x][y] == ".":
                return x, y
    for x in range(0, 9):
        for y in range(0, 9):
            if grid[x][y] == ".":
                return x, y
    return -1, -1


def isValid(grid, i, j, e):
    rowOk = all([e != grid[i][x] for x in range(9)])
    if rowOk:
        columnOk = all([e != grid[x][j] for x in range(9)])
        if columnOk:
            # finding the top left x,y co-ordinates of the section containing the i,j cell
            secTopX, secTopY = 3 * (i // 3), 3 * (j // 3)  # floored quotient should be used here.
            for x in range(secTopX, secTopX + 3):
                for y in range(secTopY, secTopY + 3):
                    if grid[x][y] == e:
                        return False
            return True
    return False


def solveSudoku(grid, i=0, j=0):
    i, j = findNextCellToFill(grid, i, j)
    if i == -1:
        return grid
    for e in range(1, 10):
        if isValid(grid, i, j, e):
            grid[i][j] = e
            if solveSudoku(grid, i, j):
                return grid
            # Undo the current cell for backtracking
            grid[i][j] = 0
    return False


def validate(grid):
    # validate all rows
    for x in range(9):
        digit_count = { 0:1, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0 }
        for y in range(9):
            if grid[x][y] == ".":
                continue
            digit_count[int(grid[x][y])] += 1
        for i in digit_count:
            if digit_count[ i ] > 1:
                return False

    # validate all columns
    for x in range(9):
        digit_count = { 0:1, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0 }
        for y in range(9):
            try:
                key = int(grid[y][x])
                digit_count[key] += 1
            except Exception:
                pass
        for i in digit_count:
            if digit_count[ i ] > 1:
                return False

    # validate all 3x3 quadrants
    def validate_quadrant( _grid, from_row, to_row, from_col, to_col ):
        digit_count = { 0:1, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0 }
        for x in range( from_row, to_row + 1 ):
            for y in range( from_col, to_col + 1 ):
                if grid[x][y] == ".":
                    continue
                digit_count[int(_grid[x][y])] += 1
        for i in digit_count:
            if digit_count[ i ] > 1:
                return False
        return True

    for x in range( 0, 7, 3 ):
        for y in range( 0, 7, 3 ):
            if not validate_quadrant(grid, x, x+2, y, y+2):
                return False
    return True


def auto_solve(board):
    res = solveSudoku(board)
    if res:
        return {"result": board_as_html(res)}
    else:
        return {"error": "Can't solve this sudoku"}


def board_as_html(board):
    html_code = ""
    for row in board:
        html_code += "<ul>"
        for col in row:
            html_code += '<li><button class="cell">{}</button></li>'.format(col)
        html_code += "</ul>"
    html_code = '<table>' + html_code + '</table>'
    return html_code


@app.route('/checkValid', methods=['POST'])
def check_valid_board():
    keys = list(request.form.to_dict().keys())
    keys.sort()
    board = []
    for key in keys:
        board.append(request.form.getlist(key))
    response = check_valid(board)
    return jsonify(response)


@app.route('/autoSolve', methods=['POST'])
def auto_solve_board():
    keys = list(request.form.to_dict().keys())
    keys.sort()
    board = []
    for key in keys:
        board.append(request.form.getlist(key))
    response = auto_solve(board)
    return jsonify(response)


@app.route('/')
def sudoku():
    board = generate_board()
    return render_template('sudoku.html', board=board)


if __name__ == '__main__':
    app.run(host='localhost', port=8082, debug=True)