import numpy as np
from sys import stdin, stdout

stonecolors = ('\033[' + '0;37m', '\033[' + '0;35m', '\033[' + '0;32m', '\033[' + '0;37m')
# Transposition table dictionary
Transposition_table = {}


# TicTacToeBoard Class represents the board for the TTT program.
class TicTacToeBoard:
	def __init__(self, size):
		self.board_size = size
		self.empty = 0
		self.x_player = 1
		self.o_player = 2

		# Initialize the TicTacToe board as a 1D numpy array filled with the Empty points.
		# This makes it easier to check legal moves and to play moves for a particular player
		self.board = np.full(self.board_size*self.board_size, self.empty, dtype = np.int32)

	# Undo a move
	def undo_move(self, move):
		self.board[move] = self.empty

	# Return the current board size
	def get_board_size(self):
		return self.board_size

	# Return the array index (pt) from the two dimensional board representation (row,col).
	# Input is a row and column, and output is the corresponding index for it.
	def get_pt(self, row, col):
		return col + (self.board_size * (row-1))

	# Return the two dimensional board representation (row, col) from the array index (pt).
	def get_coord(self, pt):	
		# The divmod() method takes two numbers and returns a pair of numbers (a tuple) consisting of their quotient and remainder.
		# Citation: https://www.programiz.com/python-programming/methods/built-in/divmod
		return divmod(pt, self.board_size)

	# Return a list of legal moves (Legal moves are all of the empty locations on the board).
	def gen_legal_moves(self):
		# Return all empty locations on the board.
		return np.where(self.board == self.empty)[0]

	# Reset the TicTacToe board to an empty board of a particular size. Must not be greater than 7 or else size will be 3
	def reset(self):
		self.board_size = 3
		self.board = np.full(self.board_size*self.board_size, self.empty, dtype = np.int32)

	# Play a move for a player at a point on the board.
	def play_move(self, player, pt):
		self.board[pt] = player

	# Check to see if a player wins on not for the current board position
	# I referenced from the simple programs ttt2 program (Cmput355/games-puzzles-algorithms/simple/ttt/ttt2)
	def is_winner(self, player):
		win = False
		winning_pos_rows = [(0, 1, 2), (3, 4, 5), (6, 7, 8)] 
		winning_pos_cols = [(0, 3, 6), (1, 4, 7), (2, 5, 8)]
		winning_pos_diags = [(2, 4, 6), (0, 4, 8)]

		# 1. Check for row win:
		for win_moves in winning_pos_rows:
			win = win or (self.board[win_moves[0]] == self.board[win_moves[1]] == self.board[win_moves[2]] == player)
		# 2. Check for column win:
		for win_moves in winning_pos_cols:
			win = win or (self.board[win_moves[0]] == self.board[win_moves[1]] == self.board[win_moves[2]] == player)
		# 3. Check for diagonal win:
		for win_moves in winning_pos_diags:
			win = win or (self.board[win_moves[0]] == self.board[win_moves[1]] == self.board[win_moves[2]] == player)
		# Return True if win is found and false if no win exists for a player
		return win


# Returns the associated integer of a particular player. For exampe: player x = 1, player 2 = 0
def player_to_int(player):
	return ['.', 'x', 'o'].index(str(player))

# Returns the associated player of a particular integer ranging from [0, 2]. For exampe: player x = 1, player 2 = 0
def int_to_player(int_code):
	return ['.', 'x', 'o'][int_code]

# Return the string format of a move. For example: If move = (2,2), then the string format for the move is c3.
def move_to_string(move):
	row, col = move
	return "abcdefghjklmnopqrstuvwxyz"[col]+ str(row+1)

# Return the two dimensional board representation (row, col) from the the string format of a move. 
# For example: If string move = c3, then the two dimensional board representation of the move (2,2)
def string_to_move(str_move, board):
	col_string, row = str_move[0], str_move[1:]
	# Check to make sure the column string is a letter between a...z, if not return -1
	if (not "a" <= col_string <= "z"): return -1

	# Convert the column string to a number format (Citation: https://stackoverflow.com/questions/4528982/convert-alphabet-letters-to-number-in-python)
	# Subtract it with leftmost column which has a string format of 'a'
	col = ord(col_string) - ord("a")

	# Check to make sure the column and row entered is within the bounds of the board.
	if not (0 <= col < board.get_board_size()): return -1
	if not row.isdigit() or not (0 < int(row) <= board.get_board_size()): return -1
	return int(row), col

# Show error message and the Help Screen to the player when a error occurs with the command line input
def error_response(message):
	print('\n\n' + stonecolors[1] + message + '\033[' + '0m')
	game_menu()

# Show the input board
# I referenced from the simple programs ttt2 program (Cmput355/games-puzzles-algorithms/simple/ttt/ttt2)
def show_board(board):
	print('\n'+stonecolors[0] + "BOARD:" + '\033[' + '0m')

	# paint outputs the a neat coloring to the board headers (Rows/Columns) and the board cells
	def paint(char): 
		if len(char)>1 and char[0]==' ': 
			return ' ' + paint(char[1:])
		x = '.xo'.find(char[0])
		if x > 0:
			return stonecolors[x] + char + '\033[' + '0m'
		elif char.isalnum():
			return '\033[' + '0;37m' + char + '\033[' + '0m'
		return char

	size = board.get_board_size()
	board_string = '   '

	# Print the Headers for the columns (Ex: a....z) depends on the size of the board
	for col in range(size):
		board_string += ' ' + paint(chr(ord('a')+col))
	board_string += '\n'

	# Iterate through the rows of the board
	for row in range(size):
		# Print the row index depends on the size of the board
		board_string += ' ' + paint(str(1+row)) + ' '
		# Iterate through the columns of the board
		for col in range(size):
			pt = board.get_pt(1+row, col)
			player = int_to_player(board.board[pt])
			board_string += ' ' + paint(player)

		board_string += '\n'
	print(board_string)

# Game Menu containing the valid input commands available to the player. 
# I referenced the help menu from the printmenu function in the ttt2 program (Cmput355/games-puzzles-algorithms/simple/ttt/ttt2)
def game_menu():
	print('\n'+stonecolors[0] + 'Commands			Descriptions' +'\033[' + '0m')
	print("--------------			---------------------------")
	print("H / h             		- Help Menu")
	print("play [x/o] [a2]    		- Play x or o at move a2")
	print("gen [x/o]			- Generate a move for player x or o using MiniMax Algorithm")
	print("genr [x/o]			- Generate a random move for player x or o")
	print("t 				- Tutor/Visualizer (Shows Legal moves and move results for both players)")
	print("show				- Show board")
	print("result 				- States the winner of the game [x/o/unknown]")
	print("r				- Reset the board")
	print("Q / q           		- Quit Program")
	print("--------------			---------------------------\n\n")

# Parse the command line string and execute the command.
def cmds(cmd_string, board):
	# Parse the command line string to obtain the command name and the arguments for the command.
	# Example: command string: "play x a2"	-> command name = "play" and the arguments = ["x", "a2"]
	cmd_list = (cmd_string.lower()).split()
	if len(cmd_list) == 0: return 
	cmd_name, cmd_args = cmd_list[0], cmd_list[1:]

	# Quit Game Command
	if cmd_name == "q":
		# Validate the command arguments 
		if len(cmd_args) != 0: return error_response("- Invalid number of Arguments for the Quit Command")
		print("GAME OVER!\n")
		exit()

	# Help Menu Command
	elif cmd_name == 'h':
		if len(cmd_args) != 0: return error_response("- Invalid number of Arguments for the Help Command")
		game_menu()

	# Play Commmand
	elif cmd_name == 'play':
		# Validate the command arguments 
		# Check to make sure the number of arguments is two (player and move) and that the move has a minimum length of two (Ex: a2, b10)
		if len(cmd_args) != 2: return error_response("- Invalid number of Arguments for the Play Command")
		if len(cmd_args[1]) < 2: return error_response("- Invalid Move Location for the Play Command")

		# Check to make sure the player is x or o
		if cmd_args[0] not in ['x', 'o']: return error_response("- Invalid Player [Valid Players:'x' or 'o']")

		# Convert the string format of the move to the two dimensional board representation (row, col)
		move = string_to_move(cmd_args[1].lower(), board)
		if move == -1: return error_response('- Invalid Move Location for the Play Command')

		pt = board.get_pt(move[0], move[1])
		player = player_to_int(cmd_args[0])

		# Check to see if the pt is a legal move. 
		if board.board[pt] != board.empty: 
			print(stonecolors[1] + '- Invalid Move Location (Move is currently occupied)' + '\033[' + '0m' +'\n')
			show_board(board)
			return 

		# Function call to the play the move for the player if no errors occured when validating the arguments
		play_move(board, player, pt)

	# Generates a move using the negamax algorithm to find best available move for a player
	elif cmd_name == 'gen':
		# Validate the command arguments 
		# Check to make sure the number of arguments is 1 (player)
		if len(cmd_args) != 1: return error_response("- Invalid number of Arguments for the Generating a move using Negamax algorithm Command")

		# Check to make sure the player is x or o
		if cmd_args[0] not in ['x', 'o']: return error_response("- Invalid Player [Valid Players:'x' or 'o']")
		player = player_to_int(cmd_args[0])

		# Compute the minimax values for a player for all legal moves.
		pts, vals = get_legal_move_outcomes(board, player, threat_check= True)

		# Check to see if there are no legal moves
		if len(pts) == 0: 
			orint(stonecolors[1] + '- No more legal moves' + '\033[' + '0m' +'\n')
			show_board(board)
			return 

		# Find all the best pts and choose one at random
		max_index = np.max(vals)
		best_indices = np.where(vals == np.max(vals))[0]
		pt =  pts[np.random.choice(best_indices)]

		# Play the best move
		stdout.write('= {}\n\n'.format(move_to_string(board.get_coord(pt))))
		stdout.flush()
		play_move(board, player, pt)

	# Generates a random move from the list of legal moves for a player and plays it for them.
	elif cmd_name == 'genr':
		# Validate the command arguments 
		# Check to make sure the number of arguments is 1 (player)
		if len(cmd_args) != 1: return error_response("- Invalid number of Arguments for the Generate Random move Command")

		# Check to make sure the player is x or o
		if cmd_args[0] not in ['x', 'o']: return error_response("- Invalid Player [Valid Players:'x' or 'o']")
		player = player_to_int(cmd_args[0])

		# Get all legal moves for the board and check to make sure their exists at least 1 legal move
		legal_moves = board.gen_legal_moves()
		if len(legal_moves) == 0:
			print(stonecolors[1] + '- No more legal moves' + '\033[' + '0m' +'\n')
			show_board(board)
			return 

		# Randomly select a move from the list of legal moves and function call to play move for the player
		pt = np.random.choice(legal_moves)
		stdout.write('= {}\n\n'.format(move_to_string(board.get_coord(pt))))
		stdout.flush()
		play_move(board, player, pt)

	# Tutor/Visualizer: Provide the legal moves for both player's and the game outcomes for the legal moves.
	elif cmd_name == 't':
		# Validate the command arguments 
		if len(cmd_args) != 0: return error_response("- Invalid number of Arguments for the Tutor/Visualizer Command")
		outcome_possibilites = { -1: "Loss", 0: "Draw", 1:"Win"}

		# Show the legal moves for a player x/o and the outocomes for the moves. Along with the suggest move to make for player x/o.
		for player in range(1,3):
			opponent = board.x_player + board.o_player - player
			pts, vals = get_legal_move_outcomes(board, player, threat_check=False)

			# Format the move and the outcomes to look visually pleasing for the player
			moves = [move_to_string(board.get_coord(pt)) for pt in pts]
			outcomes = [str(val) + " (" + outcome_possibilites[val] + ")" for val in vals]
			best_pt = None

			# Find suggest move
			# Threat Search: Check First for Win threat:
			win_moves, lose_moves = [], []
			for pt in pts:
				# Check First for Win threat:
				board.play_move(player, pt)
				if board.is_winner(player): win_moves.append(pt)
				board.undo_move(pt)

				# Check second for Lose Threat:
				board.play_move(opponent, pt)
				if board.is_winner(opponent): lose_moves.append(pt)
				board.undo_move(pt)	

			# If player has any winning moves, play any of them.
			if win_moves: best_pt = win_moves[0]
			# Else if the opponent has any next moves to win, play any of them to block it
			elif lose_moves: best_pt = lose_moves[0]
			# Find all the best pts and choose one at random
			else:
				max_index = np.max(vals)
				best_indices = np.where(vals == np.max(vals))[0]
				best_pt =  pts[np.random.choice(best_indices)]

			suggested_move = move_to_string(board.get_coord(best_pt))
			print(stonecolors[0] + "Information for player " + int_to_player(player)+ ": " + '\033[' + '0m')
			print("Legal moves: [" + ", ".join(moves) + "]")
			print("Suggested move for player " + int_to_player(player) + ": " + suggested_move)

			# Print the headers
			for title in ['Move', 'Outcome']: 
				print("\t" + stonecolors[0] + title + '\033[' + '0m', end="")

			print("\n\t-----\t-------------")
			for index in range(len(moves)):
				print("\t" + stonecolors[1] + moves[index] + "\t" + outcomes[index] + '\033[' + '0m')
			print('\n')

	# Show Board
	elif cmd_name == 'show':
		if len(cmd_args) != 0: return error_response("- Invalid number of Arguments for the Show Command")
		show_board(board)

	# State the result of the game: X won, O won, draw, unknown
	elif cmd_name == 'result':
		if len(cmd_args) != 0: return error_response("- Invalid number of Arguments for the Result Command")
		# Default result value: unknown as game is still going on
		result = "unknown" 

		legal_moves = board.gen_legal_moves()

		# Check if x won
		if board.is_winner(board.x_player): result = "x"
		# Check if o won
		elif board.is_winner(board.o_player): result = "o" 
		# Check for a draw
		elif len(legal_moves) == 0: result = "draw" 

		# Outout the result
		stdout.write('= {}\n\n'.format(result))
		stdout.flush()

	# Reset Board
	elif cmd_name == 'r':
		if len(cmd_args) != 0: return error_response("- Invalid number of Arguments for the Reset Command")
		board.reset()
		show_board(board)

	# Invalid Command Name entered, show the error message and show the help menu.
	else:
		error_response('- Invalid Command Name')


# Compute the minimax values for a player for all legal moves. Parameter threat_check is a flag to determine whether or not to do threat checking.
def get_legal_move_outcomes(board, player, threat_check):
	print("\nComputing .... It will just take a moment\n")
	vals = []
	pts = board.gen_legal_moves()
	Transposition_table = {}
	opponent = board.x_player + board.o_player - player

	if threat_check:
		# Threat Search: Check First for Win threat:
		win_moves, lose_moves = [], []
		win_vals, lose_vals = [], []
		for pt in pts:
			# Check First for Win threat:
			board.play_move(player, pt)
			if board.is_winner(player): 
				win_moves.append(pt)
				win_vals.append(1)
			board.undo_move(pt)

			# Check second for Lose Threat:
			board.play_move(opponent, pt)
			if board.is_winner(opponent): 
				lose_moves.append(pt)
				lose_vals.append(-1)
			board.undo_move(pt)	

		# If player has any winning moves, play any of them.
		if win_moves: return win_moves, win_vals
		# Else if the opponent has any next moves to win, play any of them to block it
		elif lose_moves: return lose_moves, lose_vals

	# Use Negamax algorithm to find bext move for player to make
	for pt in pts:
		# Simulate possible children moves to obtain the minimax score
		board.play_move(player, pt)

		# Obtain the minimax value for the playing at pt. And then undo the move
		vals.append(-negamax(board, opponent))
		board.undo_move(pt)

	# Return a list of legal moves and the minimax value for the moves
	return pts, vals


# Negamax algorithm: Compute the minimax value for player to move 
def negamax(board, player):
	opponent = board.x_player + board.o_player - player
	# Terminal Conditions: Check if win occured for either players (WIN/LOSS)
	if board.is_winner(player): return 1
	elif board.is_winner(opponent): return -1

	# Get all legal moves for the board and check to make sure their exists at least 1 legal move. If not (Terminal Case: DRAW)
	pts = board.gen_legal_moves()
	if len(pts) == 0: return 0

	# Convert board position to a number in base 3 (EMPTY/X/O)
	board_size = board.get_board_size()
	board_hash_code = 0
	for i in range (board_size*board_size):
		board_hash_code += (3**i)*board.board[i]

	# Check to see if the current board exists in the transposition table to avoid recomputation and if so return the minimax value for it
	if board_hash_code in Transposition_table and Transposition_table[board_hash_code]['remaining_moves']< len(pts):
		return Transposition_table[board_hash_code]['val']

	best_val = -100
	for pt in pts:
		board.play_move(player, pt)

		# Obtain the minimax value for the playing at pt
		val = -negamax(board, opponent)
		board.undo_move(pt)

		# Update the best val if the curren val is greater then the best val 
		if val > best_val: best_val = val

	Transposition_table[board_hash_code] = {'val': val, 'remaining_moves': len(pts)}
	return best_val


# Play move for a player and check if win exists.
def play_move(board, player, pt):
	board.play_move(player, pt)
	show_board(board)
	# Check if win exists
	is_win = board.is_winner(player)
	if is_win:
		stdout.write('= {}\n\n'.format(int_to_player(player)))
		stdout.flush()

		# Print winning message
		print('\n'+stonecolors[0] + 'Player '+int_to_player(player)+ ' Wins'+'\033[' + '0m')
		play_again(board)


# Ask player to play again or quit. According to their response either reset the board for a new game or quit the program.
def play_again(board):
	# Check if player wants to play again
	while True:
		play_again = input(stonecolors[0] + 'Do you want to play again (y/n): ' +'\033[' + '0m')
		play_again = play_again.lower()
		# Play again
		if play_again == "y": 
			board.reset()
			print("NEW GAME: ")
			show_board(board)
			return
		# Quit Program
		elif play_again == "n": 
			print("GAME OVER!\n")
			exit()
		# Invalid Input
		else: print(stonecolors[1] + 'Invalid Input' + '\033[' + '0m')


# Intro message to the player
def intro_prompt():
	print(stonecolors[0] + 'Welcome to HM\'s TTT Program!' + '\033[' + '0m')
	print(stonecolors[0] + 'Program Commands are the following:' + '\033[' + '0m')
	game_menu()


# The interact function handles all player interaction with the TTT program
def interact():
	# Instantiate a TicTacToe board (board size is 3x3)
	board = TicTacToeBoard(3)

	# Show Prompt messages to welcome the player and show the help menu
	intro_prompt()
	show_board(board)

	# Read command line infinitely until player decides to quit
	cmd_line= stdin.readline()
	while cmd_line:
		# Function call to parse and execute the player's command
		cmds(cmd_line, board)
		cmd_line = stdin.readline()


# Function call to start the player interaction with the TicTacToe program 
interact()