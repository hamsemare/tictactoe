# I referenced how to spawn child applicatins for testing (Citation: http://www.bx.psu.edu/~nate/pexpect/pexpect.html)
import pexpect
TIMEOUT=45

# Flags for keeping count of score
wins_x=0
wins_o=0
draws = 0

# Generate a move using the negamax algorithm to find best available move for a player
def gen_move(program, player):
	program.sendline('gen ' + player)
	program.expect([pexpect.TIMEOUT,'= [a-z][0-9]'])
	print("Player " + player + ": " + program.after.decode("utf-8")[2:] + "\n")
	return program.after.decode("utf-8")[2:]

# Generates a random move
def gen_random_move(program, player):
	program.sendline('genr ' + player)
	program.expect([pexpect.TIMEOUT,'= [a-z][0-9]'])
	print("Player " + player + ": " + program.after.decode("utf-8")[2:] + "\n")
	return program.after.decode("utf-8")[2:]

# Play a move for a player for a program
def play_move(program, player, move):
	program.sendline('play ' + player + ' ' + move)

# Simulate a game between two players x and o
def play_games(number_of_games):
	global wins_x, wins_o, draws
	for game in range(1, number_of_games+1):
		print("\nGAME #" + str(game) + ": ")
		# Instantiate player x and player o and the observer
		player_x_program = pexpect.spawn('python3 ttt.py')
		player_o_program = pexpect.spawn('python3 ttt.py')
		observer_program = pexpect.spawn('python3 ttt.py')

		turn = 0
		result = None
		# Loop until endgame occurs (WIN/LOSS/DRAW)
		while True:
			# x players turn to generate a move and play
			if turn == 0:
				move = gen_random_move(player_x_program, 'x')
				# Play the move on the o program and the observer programs as well
				play_move(player_o_program,'x', move)
				play_move(observer_program,'x', move)
			# o players turn to generate a move and play
			else:
				move = gen_move(player_o_program,'o')
				# Play the move on the x program and the observer programs as well
				play_move(player_x_program,'o', move)
				play_move(observer_program,'o', move)
			# Alternate turns
			turn = 1 - turn

			# Find winner 
			observer_program.sendline('result')
			observer_program.expect(['= x','= o','= unknown', '= draw'])
			status = observer_program.after.decode("utf-8")[2:]
			if status == 'x':
				result = 1
				break
			elif status == 'o':
				result = 2
				break
			elif status == 'draw':
				result = 3
				break

		# Increment the win score for the player that has won the game or draw if neither won
		if result == 1:
			print("Result: Player x wins") 
			wins_x += 1
		elif result == 2:
			print("Result: Player o wins")  
			wins_o += 1
		else: 
			print("Result: Draw")  
			draws += 1


# Call to play 10 games to see winner
play_games(number_of_games=50)

# Print Game results
print('Player x wins: ' + str(wins_x))
print('Player o wins: ' + str(wins_o))
print('Draws: ' + str(draws))

# Save Results
f = open("game_results_weak_vs_strong.txt", "w")
f.write("player x: Player using random move selection (Weak Player) \n")
f.write("player o: Player using Negamax and Threat Search (Strong Player) \n")
f.write("Player x wins: {}\n".format(str(wins_x)))
f.write("Player o wins: {}\n".format(str(wins_o)))
f.write("Draws: {}\n".format(str(draws)))
f.close()


