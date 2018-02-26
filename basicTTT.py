#！/usr/bin/python3

import numpy as np 
import sys

class Board(object):
	def __init__(self):
		self.board = [ '-' for i in range(9)]

	def putIn(self, action, chess):
		if self.board[action] == '-':
			self.board[action] = chess

	def is_legal(self,action):
		return self.board[action] == '-'

	def showBoard(self):
		return self.board[:]

	def get_ava_Action(self):
		actions = []
		for i in range(9):
			if self.board[i] == '-':
				actions.append(i)
		return actions

	def vanishMove(self,action):
		self.board[action] = '-'
		

	def termiate(self):
		board = self.board
		win_lines = [board[0:3], board[3:6], board[6:9], board[0::3],board[1::3],board[2::3], board[0::4], board[2:7:2]]

		if ['X']*3 in win_lines or ['O']*3 in win_lines or '-' not in board:
			return True
		else:
			return False

	def winner(self):
		board = self.board
		win_lines = [board[0:3], board[3:6], board[6:9], board[0::3], board[1::3], board[2::3], board[0::4],					 board[2:7:2]]

		if['X']*3 in win_lines:
			return 1
		elif['O']*3 in win_lines:
			return -1
		else:
			return 0

	def print_board(self):
		board = self.board
		# print_board = np.array()
		for i in range(len(board)):
			sys.stderr.write(board[i])
			sys.stderr.write(" ")
			if (i+1)%3 == 0:
				sys.stderr.write("\n")
				sys.stderr.flush()


class chessPlayer(object):
	def __init__(self, chess='X'):
		self.chess = chess

	def think(self, board):
		pass

	def putChoice(self, board, action):
		board.putIn(action, self.chess)
		sys.stdout.write(str(action+1)+'\n')
		sys.stderr.write('\n')
		sys.stdout.flush()

class human(chessPlayer):
	def __init__(self, chess):
		super().__init__(chess)

	def think(self,board):
		while True:
			sys.stderr.write("Please enter your next choice:")
			sys.stderr.flush()
			action = sys.stdin.readline()[:-1]

			if len(action)==1 and action in '123456789' and board.is_legal(int(action)-1):
				action = int(action) -1
				return int(action)

			# else:



class AI(chessPlayer):
	def __init__(self, chess):
		super().__init__(chess)

	def think(self,board):
		sys.stderr.write("AI's move is:\n")
		chess = ['X', 'O'][self.chess == 'X']
		player = AI(chess)
		action = self.minimax(board,player)[1]

		return action

	def minimax(self, board, player, depth=0):
		if self.chess == "O":
			winValue = -10
		else:
			winValue = 10
		if board.termiate():
			if board.winner() == 1:
				return -10 + depth, None
			elif board.winner() == -1:
				return 10 - depth, None
			elif board.winner() == 0:
				return 0, None
		
		for action in board.get_ava_Action():
			board.putIn(action, self.chess)
			val = player.minimax(board, self, depth+1)[0]
			board.vanishMove(action)         

			if self.chess == "O":
				if val > winValue:
					winValue, winAction = val, action
			else:
				if val < winValue:
					winValue, winAction = val, action
		return [winValue,winAction]
		

class Game(object):
	def __init__(self):
		self.board = Board()
		self.current_Player = None

	def playerOrder(self, upper, chess = 'X'):
		if  upper == 'Human':
			return human(chess)
		else:
			return AI(chess)

	def playerChange(self,playerOne, playerTwo):
		if self.current_Player is None:
			return playerOne
		else:
			return [playerOne,playerTwo][self.current_Player == playerOne]

	def printWinner(self, winner):
		if winner == 1:
			sys.stderr.write("Winner is: upper ! \n")
		elif winner == -1:
			sys.stderr.write("Winner is: lower ! \n")
		else:
			sys.stderr.write("It is a tie! \n")

	def run(self):
		while True:
			sys.stderr.write("Choose X or O ?")
			sys.stderr.flush()
			chooseUpper = sys.stdin.readline()[:-1]
			if chooseUpper == 'X' or chooseUpper == 'x':
				playerOne = self.playerOrder('Human', 'X')
				playerTwo = self.playerOrder('AI', 'O')
				break
			elif chooseUpper == 'O' or chooseUpper == 'o':
				playerOne = self.playerOrder('AI', 'X')
				playerTwo = self.playerOrder('Human', 'O')
				break
			else:
				sys.stderr.write("Wrong! Please enter your choice again:")
				sys.stderr.flush()

		sys.stderr.write("\n Game Starting! \n")
		self.board.print_board()

		while True:
			self.current_Player = self.playerChange(playerOne, playerTwo)
			action = self.current_Player.think(self.board)
			self.current_Player.putChoice(self.board, action)
			self.board.print_board()

			if self.board.termiate():
				winner = self.board.winner()
				break

		self.printWinner(winner)

		sys.stderr.write("Game Over \n")
		sys.stderr.flush()

if __name__ == '__main__':
	while True:
		Game().run()

	





