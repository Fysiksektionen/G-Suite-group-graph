

class Graph:
    def __init__(self, directed=True, **kwattrs):
        self.directed = directed
        self.nodes = {}
        self.edges = set()
        self.attrs = kwattrs

    def addNode(self, nodeID, value, **kwattrs):
        node = Node(nodeID, value, **kwattrs)
        self.nodes[nodeID] = node
        return node

    def addEdge(self, node1ID, node2ID, **kwattrs):
        for nodeID in [node1ID, node2ID]:
            if nodeID not in self.nodes:
                self.addNode(nodeID, None)
        node1 = self.nodes[node1ID]
        node2 = self.nodes[node2ID]
        edge = Edge(node1ID, node1, node2ID, node2, **kwattrs)
        self.edges.add(edge)
        return edge

    def __str__(self):
        attr_str = "\n\t".join([f"{key} = {self.attrs[key]}" for key in self.attrs])
        nodes_str = "\n\t".join([str(node) for node in self.nodes.values()])
        edges_str = "\n\t".join([str(edge) for edge in self.edges])
        dot = f"digraph G {{\n\t{nodes_str}\n\t{edges_str}\n}}"
        return dot


class Node:
    def __init__(self, nodeID, value, **kwattrs):
        self.nodeID = nodeID
        self.value = value
        self.attrs = kwattrs

    def __str__(self):
        attr_str = " ".join([f'{key} = "{self.attrs[key]}"' for key in self.attrs])
        dot = f'"{self.nodeID}" [ {attr_str} ];'
        return dot


class Edge:
    def __init__(self, node1ID, node1, node2ID, node2, **kwattrs):
        self.node1ID = node1ID
        self.node2ID = node2ID
        self.node1 = node1
        self.node2 = node2
        self.attrs = kwattrs

    def __repr__(self):
        return self.node1ID + self.node2ID

    def __hash__(self):
        return hash(self.__repr__())

    def __str__(self):
        attr_str = " ".join([f"{key} = {self.attrs[key]}" for key in self.attrs])
        dot = f'"{self.node1ID}" -> "{self.node2ID}" [ {attr_str} ];'
        return dot