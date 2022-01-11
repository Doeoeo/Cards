import collections

class Node:
	
	def __init__(self, index:int):
		self.visited = False
		self.index = index
		self.neighbours = []

	def addNode(self, node):
		self.neighbours.append(node)

	def visitNode(self, x:collections.deque):
		self.visited = True
		x.append(self.index)
		#print(x)
		for i in self.neighbours:
			if not i.getVisited():
				i.visitNode(x)
	

	def getVisited(self):
		return self.visited

	def __repr__(self):
		return str(self.index)



def findComponents(v:tuple, e:tuple):
	nodes = [Node(int(i)) for i in v]
	for i in e:
		nodes[i[0]].addNode(nodes[i[1]])
		nodes[i[1]].addNode(nodes[i[0]])
	graph = collections.deque()
	for i in nodes:
		if not i.getVisited():
			x = collections.deque()
			i.visitNode(x)
			graph.append(x)

	listedGraph = []

	for i in graph:
		listedGraph.append(list(i))

	return listedGraph
