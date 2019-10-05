

class Graph:
    def __init__(self, directed=True):
        self.directed = directed
        self.nodes = {}
        self.edges = []

    def addNode(self, nodeID, *attrs, **kwattrs):
        node = Node(*attrs, **kwattrs)
        self.nodes[nodeID] = node
        return node

    def addEdge(self, node1ID, node2ID, *attrs, **kwattrs):
        for nodeID in [node1ID, node2ID]:
            if nodeID not in self.nodes:
                addNode(nodeID)
        node1 = self.nodes[node1ID]
        node2 = self.nodes[node2ID]
        edge = Edge(node1, node2, *attrs, **kwattrs)
        self.edges.append(edge)
        return edge

    def __str__(self):
        pass


class Node:
    def __init__(self, *attrs, **kwattrs):
        pass

    def __str__(self):
        pass


class Edge:
    def __init__(self, node1, node2, *attrs, **kwattrs):
        self.node1 = node1
        self.node2 = node2

    def __str__(self):
        pass