# -*- coding: utf-8 -*-
def create_board(n):
  board = []
  for i in range(n):
    row = []
    for j in range(n):
      row.append(None)
    board.append(row)
  return board

def print_board(board):
  n = len(board)
  print("###START###")
  for i in range(n):
    for j in range(n):
      print(board[i][j] or "-", end=" ")
    print("")
  print("###END###")

def add_shape(board, shape, row, col):
  board[row][col] = shape

def is_full(board):
  n = len(board)
  for i in range(n):
    for j in range(n):
      if not board[i][j]:
        return False
  return True

def has_winner(board):
  n = len(board)
  def row_winner(board):
    i = 0
    while i < n:
      res = True
      init_shape = board[i][0]
      if not init_shape:
        res = False
      j = 1
      while j < n:
        shape = board[i][j]
        if shape != init_shape:
          res = False
        j += 1
      if res:
        return init_shape
      i += 1
    return False      

  def col_winner(board):
    #TODO
    pass
  return row_winner(board) or col_winner(board)

def game():
  players = ["name1", "name2"]
  shapes =   ["X",    "O"]

  counter = 0
  n = 3
  b = create_board(n)
  while not is_full(b) and not has_winner(b):    
    print_board(b)    
    print("Player {} is now playing".format(players[counter]))
    ## more ways to format    
    #print("Player ", players[counter], " is now playing")
    #print(f"Player {players[counter]} is now playing")
    
    row = int(input("please insert row")) - 1
    col = int(input("please insert col")) - 1
    add_shape(b, shapes[counter], row, col)
    counter += 1
    if counter >= len(players):
      counter = 0

  res = has_winner(b)
  if res:
    print("Shape {} won!".format(res))

if __name__ == '__main__':
  game()

