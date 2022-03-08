from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

def generate_board():
    # TODO generate a valid board
    board = [["8","3",".",".","7",".",".",".","."]
,["6",".",".","1","9","5",".",".","."]
,[".","9","8",".",".",".",".","6","."]
,["8",".",".",".","6",".",".",".","3"]
,["4",".",".","8",".","3",".",".","1"]
,["7",".",".",".","2",".",".",".","6"]
,[".","6",".",".",".",".","2","8","."]
,[".",".",".","4","1","9",".",".","5"]
,[".",".",".",".","8",".",".","7","9"]]
    return board

def check_valid(board):
    # TODO check if the board is valid
    return {"result": True}


def auto_solve(board):
    # TODO auto solve board
    solved_board = [["5","3","4","6","7","8","9","1","2"],["6","7","2","1","9","5","3","4","8"],["1","9","8","3","4","2","5","6","7"],["8","5","9","7","6","1","4","2","3"],["4","2","6","8","5","3","7","9","1"],["7","1","3","9","2","4","8","5","6"],["9","6","1","5","3","7","2","8","4"],["2","8","7","4","1","9","6","3","5"],["3","4","5","2","8","6","1","7","9"]]
    return {"result": board_as_html(solved_board)}


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
    app.run(host='localhost', port=8081, debug=True)