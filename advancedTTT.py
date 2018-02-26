#！ /usr/bin/python3

import numpy as np 
import sys
import random

class Board(object):
	def __init__(self):
		self.board = [['-' for i in range(9)] for i in range(9)]
		self.manual = []

	def putIN(self, b_num, action, chess):
		if self.board[b_num][action] == '-':
			self.board[b_num][action] = chess
			self.manual.append((b_num,action,chess))

	def is_legal(self, b_num, action):
		return self.board[b_num][action] == '-'

	def showBoard(self):
		return self.board[:][:]

	def get_ava_Action(self, b_num):
		actions = []
		if '-' in self.board[b_num]:
			for i in range(9):
				if self.board[b_num][i] == '-':
					actions.append([b_num, i])
		# if board b_num is full, next player can choose wherever to play
		else:
			for i in range(9):
				for j in range(9):
					if self.board[i][j] == '-':
						actions.append([i,j])
		return actions

	def vanishMove(self, b_num, action):
		self.board[b_num][action] = '-'

	def terminate(self):
		flag = 1 
		for i in range(9):
			board = self.board
			win_lines = [board[i][0:3], board[i][3:6], board[i][6:9], board[i][0::3],board[i][1::3],board[i][2::3],board[i][0::4],board[i][2:7:2]]
			if ['X']*3 in win_lines or ['O']*3 in win_lines:
				return True
			elif '-' in board[i]:
				flag = 0
			
		if flag: 
			return True
		else:	
			return False

	def winner(self):
		board = self.board
		for i in range(9):
			win_lines = [board[i][0:3], board[i][3:6], board[i][6:9], board[i][0::3],board[i][1::3],board[i][2::3],board[i][0::4],board[i][2:7:2]]
			if ['X']*3 in win_lines:
				return 1
			elif['O']*3 in win_lines:
				return -1
		return 0
			


	def print_board(self):
		board = self.board
		sys.stderr.write("\n")
		for i in range(3):	
			for j in range(3):
				for k in range(3*i, 3*i+3):
					# sys.stderr.write(str(j))
					sys.stderr.write(board[j][k])
					sys.stderr.write(" ")
				sys.stderr.write("|")
			sys.stderr.write("\n")
		sys.stderr.write("--------------------\n")

		for i in range(3):
			for j in range(3,6):
				for k in range(3*i, 3*i+3):
					# sys.stderr.write(str(j))
					sys.stderr.write(board[j][k])
					sys.stderr.write(" ")
				sys.stderr.write("|")
			sys.stderr.write("\n")
		sys.stderr.write("--------------------\n")

		for i in range(3):
			for j in range(6,9):
				for k in range(3*i, 3*i+3):
					# sys.stderr.write(str(j))
					sys.stderr.write(board[j][k])
					sys.stderr.write(" ")
				sys.stderr.write("|")
			sys.stderr.write("\n")
		sys.stderr.write("--------------------\n")

class chessPlayer(object):
	def __init__(self, chess='X'):
		self.chess = chess 

	def think(self, board):
		pass

	def putChoice(self, b_num, board, action):
		sys.stderr.write(self.chess+' '+"The last move is: ")
		sys.stderr.flush()
		sys.stdout.write(str(b_num+1)+' '+str(action+1))
		sys.stdout.flush()
		board.putIN(b_num, action, self.chess)

class human(chessPlayer):
	def __init__(self, chess):
		super().__init__(chess)

	def think(self, board, b_num):
		global board_num
		# print("human"+str(board_num))
		b_num = board_num
		# print(b_num)
		while True:
			while '-' not in board.board[b_num]:
				sys.stderr.write('Board' + str(b_num) + 'full, plase choose choice you want to play on.')
				sys.stderr.flush()
				choice = sys.stdin.readline()[:-1]
				board_num = int(choice[0])-1
				b_num = board_num
				action = int(choice[2]) - 1


			# sys.stderr.write("Please enter your next choice:")
			if b_num == -1:
				sys.stderr.write("Please enter your choice:")
				sys.stderr.flush()
				choice = sys.stdin.readline()[:-1]
				board_num = int(choice[0])-1
				b_num = board_num
				action = int(choice[2])-1
			else:
				choice = [-1, -1];
				temp = board_num
				while (int(choice[0])-1)!=temp:
					sys.stderr.write("Please enter your choice:")
					sys.stderr.flush()
					choice = sys.stdin.readline()[:-1]
					board_num = int(choice[0]) - 1
					b_num = board_num
					action = int(choice[2]) - 1
			# action = sys.stdin.readline()[:-1]
			
			if action in range(9) and board.is_legal(b_num, int(action)):
				action_right = int(action)
				return [b_num, action_right]

class AI(chessPlayer):
	def __init__(self,chess):
		super().__init__(chess)

	def think(self, board, b_num, depth=5):
		global board_num
		# print("AI"+str(board_num))
		return self.max_value(board, board_num, -10000, 10000, depth)[1]

	def max_value(self, board, b_num, alpha, beta, depth):
		if board.terminate() or depth == 0:
			return [self.utility(board),[None,None]]

		val = -10000
		move = board.get_ava_Action(b_num)[0]
		for action in board.get_ava_Action(b_num):
			board.putIN(action[0], action[1], self.chess)
			tmp_val = self.min_value(board,action[1], alpha, beta, depth-1)
			# print(type(tmp_val))
			test = tmp_val[0]
			board.vanishMove(action[0],action[1])
			if test > val:
				move = action
				val = test

			if val >= beta:
				return [val,move]
			alpha = max(alpha, val)
		return [val,move]

	def min_value(self, board, b_num, alpha, beta, depth):
		if board.terminate() or depth ==0:
			return [self.utility(board),[None,None]]

		val = 10000
		move = board.get_ava_Action(b_num)[0]
		for action in board.get_ava_Action(b_num):
			board.putIN(action[0], action[1], ['X','O'][self.chess == 'X'])
			tmp_val = self.max_value(board, action[1], alpha, beta, depth-1)
			# print(type(tmp_val))
			test = tmp_val[0]
			# tmp_val = min(val, self.max_value(board, action[1], alpha, beta, depth-1)[0])
			board.vanishMove(action[0],action[1])
			if test < val:
				move = action
				val = test
	
			if val <= alpha:
				return [val, move]
			beta = min(beta, val)
		return [val, move] 

	def utility(self, board):
		state = board.board
		point = 0 
		op_chess = ['X','O'][self.chess == 'X']
		for i in range(9):
			if state[i][i] == self.chess:
				point += 1;
			elif state[i][i] == op_chess:
				point -= 1;

			if state[i][4] == self.chess:
				point += 1;
			elif state[i][4] == op_chess:
				point -= 1;

			point += (state[i].count(self.chess) - state[i].count(op_chess)-1)*4
			win_lines = [state[i][0:3],state[i][3:6],state[i][6:9],state[i][0::3],state[i][1::3], state[i][2::3], state[i][0::4], state[i][2:7:2]]

			if self.chess*3 in win_lines:
				point += 30
			elif op_chess*3 in win_lines:
				point -= 30

		return point
			


class Game(object):
	def __init__(self):
		self.board = Board()
		self.current_Player = None

	def playerOrder(self, upper, chess = 'X'):
		if upper == 'Human':
			return human(chess)
		else:
			return AI(chess)

	def playerChange(self,playerOne,playerTwo):
		if self.current_Player is None:
			return playerOne
		else:
			return [playerOne,playerTwo][self.current_Player == playerOne]

	def printWinner(self, winner):
		if  winner == 1:
			sys.stderr.write("winner is uppper!\n")
		elif winner == -1:
			sys.stderr.write("winner is lower! \n")
		else:
			sys.stderr.write("It is a tie! \n")

	def run(self):
		global board_num
		while True:
			sys.stderr.write("choose X or O?")
			sys.stderr.flush()
			chooseUpper = sys.stdin.readline()[:-1]
			if chooseUpper == 'X' or chooseUpper == 'x':
				playerOne = self.playerOrder('Human', 'X')
				playerTwo = self.playerOrder('AI', 'O')
				# sys.stderr.write("Choose the fist board you want to play on.")
				# sys.stderr.write('Choose the first step')
				# sys.stderr.flush()
				# choice = int(sys.stdin.readline()[:-1])
				# board_num = choice[1]-1
				# board_num = int(sys.stdin.readline()[:-1]) -1 
				break
			elif chooseUpper == 'O' or chooseUpper == 'o':
				playerOne = self.playerOrder('AI', 'X')
				playerTwo = self.playerOrder('Human', 'O')
				break
			else:
				sys.stderr.write("Error!")
				sys.stderr.flush()
		sys.stderr.write("\n Game start \n")
		self.board.print_board()

		while True:
			self.current_Player = self.playerChange(playerOne, playerTwo)
			# action = self.current_Player.think(self.board, b_num = -1)[1]
			think_result = self.current_Player.think(self.board, b_num = -1)
			action = think_result[1]
			temp = think_result[0]
			self.current_Player.putChoice(temp, self.board, action)
			# board_num = action
			self.board.print_board()

			if self.board.terminate():
				winner = self.board.winner()
				break
			board_num = action

		self.printWinner(winner)
		sys.stderr.write("Good Game \n")
		sys.stderr.flush()

board_num = -1 
if __name__ == '__main__':
	while True:
		Game().run()




