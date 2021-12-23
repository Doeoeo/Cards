from typing import List
from itertools import combinations
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.pyplot import figure
import numpy as np

class Card:
	# Drawing data
	w = 3
	h = 3
	pointDistance = 4 * 3 / 8
	halfDistance = pointDistance / 2
	colour = ["green", "blue", "red", "orange", "blue", "green", "orange", "red"]

	def __init__(self, innerCon: List[int]):
		self.innerCon = innerCon
		self.outerCon = [Card] * 8

		# Drawing data for points and lines
		self.pointPos = [
			[0, 0, self.halfDistance, 3 * self.halfDistance, 2 * self.pointDistance, 2 * self.pointDistance, 3 * self.halfDistance, self.halfDistance],
			[self.halfDistance, 3 * self.halfDistance, 2 * self.pointDistance, 2 * self.pointDistance, 3 * self.halfDistance, self.halfDistance, 0, 0]
		]

		# The 5-th point is the center extra point
		self.socketCon = [set() for i in range(5)]

		# Drawing data for squished blue sx
		self.mergePos = [
			[0, self.pointDistance, 2 * self.pointDistance, self.pointDistance, self.pointDistance],
			[self.pointDistance, 2 * self.pointDistance, self.pointDistance, 0, self.pointDistance]
		]

		# Merging of the inner connections to 5 (left, down, right, up)
		self.merge()

	#def connect(left: Card, down: Card, right: Card, up: Card):
	# Used to connect cards
	def connect(self, cards: List):
		for i in range(len(cards)):
			self.outerCon[i] = cards[i]
			self.outerCon[i + 1] = cards[i]

	# Might be useful :)
	def left(self): return self.outerCon[0]
	def down(self): return self.outerCon[2]
	def right(self): return self.outerCon[4]
	def up(self): return self.outerCon[6]

	# Draw function for cards, points, lines and blue sx
	def draw(self, x: float, y: float):
		# Draw card shape
		plt.gca().add_patch(patches.Rectangle((x, y), self.h, self.w, linewidth=1, edgecolor='black', facecolor='none'))
		# Draw points
		plt.scatter([d + x for d in self.pointPos[0]], [d + y for d in self.pointPos[1]], c = self.colour)
		# Draw merged points
		plt.scatter([d + x for d in self.mergePos[0]], [d + y for d in self.mergePos[1]], c = "black")
		# Draw lines
		for i in range(len(self.innerCon)):
			plt.plot([self.pointPos[0][i] + x, self.pointPos[0][self.innerCon[i]] + x], 
					 [self.pointPos[1][i] + y, self.pointPos[1][self.innerCon[i]] + y], c = "red")
		# Draw merged lines
		for i in range(len(self.socketCon) - 1):
			xPts = [self.mergePos[0][i] + x, self.mergePos[0][min(self.socketCon[i])] + x]
			yPts = [self.mergePos[1][i] + y, self.mergePos[1][min(self.socketCon[i])] + y]
			plt.plot(xPts, yPts, c = "blue")

	# Merging of inner connections
	def merge(self):
		# Map each inner point to a general l, d, r, u point
		for i in range(len(self.innerCon)):
			self.socketCon[(int)(i / 2)].add((int)(self.innerCon[i] / 2))
		
		# If land covers two merged positions we redirect it to a central point
		for i in range(len(self.socketCon) - 1):
			if (len(self.socketCon[i]) != 1): self.socketCon[i] = {4}

	# Print override
	def __repr__(self):
		return str(self.innerCon) + "\n"

def drawCards(layout): 
# For printing a single card
#	layout[1][0].draw(layout[1][0].w, layout[1][0].h)
	for i in range(len(layout)):
		for j in range(len(layout[i])):
			layout[i][j].draw(layout[i][j].w * j, layout[i][j].h * i)

	plt.plot(0, 0)
	plt.gcf().set_size_inches(15,5)
	plt.show()

# Recursive function to generate all inner connection for the card layout
def generateCards(build: List[int], toBuild: List[int], cards: set):
	if (len(build) == 0) : 
		cards.add(tuple(toBuild))
		return

	for i, j in combinations(build, 2): 
		if ((j - i) % 2 == 1):
			skip = False
			# This checks if our possible line is crossing an already existing line
			for k in range(i + 1, j): 
				if (toBuild[k] != -1): skip = True
			if (skip): continue

			tmp = build.copy()
			tmp.remove(i)
			tmp.remove(j)
			tmpBuild = toBuild.copy()
			tmpBuild[i] = j
			tmpBuild[j] = i

			generateCards(tmp, tmpBuild.copy(), cards)
			

cardSet = set()
# Create card inner layouts
generateCards([0, 1, 2, 3, 4, 5, 6, 7], [-1] * 8, cardSet)
# Shuffle the cards for a random order
cards = [Card(list(i)) for i in cardSet]
random.shuffle(cards)

# Connect the cards between one another
layout = [[Card] * 7 for i in range(2)]
for i in range(len(cards)): layout[int(i / 7)][i % 7] = cards[i]
for i in range(len(cards)): 
	h = (int)(i / 7)
	w = i % 7
	cards[i].connect([layout[h][(w - 1) % 7], layout[(h + 1) % 2][w], layout[h][(w + 1) % 7], layout[(h - 1) % 2][w]])

drawCards(layout)
#cards.randomize()
#layout = [7][2]


#plt.plot([0, 0], [10, 10])



