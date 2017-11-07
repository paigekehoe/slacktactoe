## Class file for Tic Tac Toe Game Object
## Author: Paige Kehoe
## Date: 11/6/17

class Game:

	def __init__(self):
		self.turn_count=0 #turn counting variable
		self.player_0 = '' #challenger is saves as P0 and plays Os
		self.player_1 = '' #responder is saved as P1 and plays Xs
		self.board = [9] * 9 #creates a list for a 3X3 game board with 9 in every spot
		self.end_condition = None #integer variable to hold number codes for end game condidition
		# Board Index Key:
		# 0    1    2
		# 3    4    5
		# 6    7    8

	def set_up(self, id0, id1):
		self.player_0 = id0
		self.player_1 = id1
		

	def check_win(self):
		#summing up each potential win combination to check for win scenario
		board = self.board
		sums = [
			board[0] + board[1] + board[2], #top row win
			board[3] + board[4] + board[5], #middle row win
			board[6] + board[7] + board[8], #bottom row win
			board[0] + board[3] + board[6], #left col win
			board[1] + board[4] + board[7], #middle col win
			board[2] + board[5] + board[8], #right col win
			board[0] + board[4] + board[8], #diagonal win
			board[6] + board[4] + board[2], #diagonal win
			]
		counter = sums[0];
		for sum in sums:
			if(sum==0):
				#player 0 wins and we return 0 as the winner sum
				self.end_condition=sum
				return True
			if(sum==3):
				#player 1 wins and we return 1 as the winner sum
				self.end_condition=sum
				return True
			counter += sum #if full board sums to 4, and we haven't hit win condition, tie game
			self.end_condition = sum
		return False

	def turn(self, spot):
		self.board[spot-1] = self.turn_count%2
		self.turn_count+=1
		return self.board

	def is_free(self, spot):
		if spot >10:
			#this spot is outside the board size
			return None
		elif self.board[spot-1] == 9:
			return True
		else:
			return False





