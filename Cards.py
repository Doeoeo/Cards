from typing import List
from itertools import combinations
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.pyplot import figure
import numpy as np

class Card:
	w = 3
	h = 3
	pointDistance = 4 * 3 / 8
	halfDistance = pointDistance / 2
	colour = ["green", "blue", "red", "orange", "blue", "green", "orange", "red"]
	def __init__(self, innerCon: List[int]):
		self.innerCon = innerCon
		self.outerCon = [Card] * 8
		self.pointPos = [
			[self.halfDistance, 3 * self.halfDistance, 2 * self.pointDistance, 2 * self.pointDistance, 3 * self.halfDistance, self.halfDistance, 0, 0],
			[0, 0, self.halfDistance, 3 * self.halfDistance, 2 * self.pointDistance, 2 * self.pointDistance, 3 * self.halfDistance, self.halfDistance]
		]
		self.socketCon = [int] * 8

	#def connect(left: Card, down: Card, right: Card, up: Card):
	def connect(self, cards: List):
		for i in range(len(cards)):
			self.outerCon[i] = cards[i]
			self.outerCon[i + 1] = cards[i]

	def left(self): return self.outerCon[0]
	def down(self): return self.outerCon[2]
	def right(self): return self.outerCon[4]
	def up(self): return self.outerCon[6]

	def draw(self, x: float, y: float):
		print("drawing", x, " ", y, " ", self.w, " ", self.h)
		# Draw card shape
		plt.gca().add_patch(patches.Rectangle((x, y), self.h, self.w, linewidth=1, edgecolor='black', facecolor='none'))
		# Draw points
		plt.scatter([d + x for d in self.pointPos[1]], [d + y for d in self.pointPos[0]], c = self.colour)
		# Draw lines
		for i in range(len(self.innerCon)):
			plt.plot([self.pointPos[1][i] + x, self.pointPos[1][self.innerCon[i]] + x], 
					 [self.pointPos[0][i] + y, self.pointPos[0][self.innerCon[i]] + y], c = "red")

	def __repr__(self):
		return str(self.innerCon) + "\n"

def generateCards(build: List[int], toBuild: List[int], cards: set):
	if (len(build) == 0) : 
		cards.add(tuple(toBuild))
		return

	for i, j in combinations(build, 2): 
		if ((j - i) % 2 == 1):
			skip = False
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
generateCards([0, 1, 2, 3, 4, 5, 6, 7], [-1] * 8, cardSet)
cards = ([Card(list(i)) for i in cardSet])
#random.shuffle(cards)
#print(cards)
print("len", len(cards))
layout = [[Card] * 7 for i in range(2)]
for i in range(len(cards)): layout[int(i / 7)][i % 7] = cards[i]
for i in range(len(cards)): 
	h = (int)(i / 7)
	w = i % 7
	cards[i].connect([layout[h][(w - 1) % 7], layout[(h + 1) % 2][w], layout[h][(w + 1) % 7], layout[(h - 1) % 2][w]])



#cards.randomize()
#layout = [7][2]

for i in range(len(layout)):
	for j in range(len(layout[i])):
		print(layout[i][j])
		layout[i][j].draw(layout[i][j].w * j, layout[i][j].h * i)
#plt.plot([0, 0], [10, 10])
plt.plot(0, 0)
plt.gcf().set_size_inches(15,5)
#plt.gca().add_patch(patches.Rectangle((0.2, 0.2), 0.5, 0.5, linewidth=1, edgecolor='r', facecolor='none'))
plt.show()


