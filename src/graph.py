from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class Node:
    data: any


class Graph:
    adjacencyList: dict[Node, set[Node]] = {}

    def __init__(self, data: any):
        self.adjacencyList = {Node(data): set()}


    @classmethod
    def createAround(cls, data: any) -> tuple[Self, Node]:
        graph = cls(data)
        first_node = list(graph.adjacencyList.keys())[0]
        return (graph, first_node)
    
    
    def addNode(self, data: any) -> Node:
        node = Node(data)
        self.adjacencyList[node] = set()
        return node
    
    
    def connectNodes(self, node1: Node, node2: Node) -> bool:
        allNodes = self.adjacencyList.keys()

        if not (node1 in allNodes and node2 in allNodes):
            return False
        
        self.adjacencyList[node1].add(node2)
        self.adjacencyList[node2].add(node1)


    def addConnected(self, data: any, to: Node) -> tuple[bool, Node | None]:
        if not to in self.adjacencyList.keys():
            return (False, None)
        
        node = Node(data)
        self.adjacencyList[node] = set([to])
        self.adjacencyList[to].add(node)

        return (True, node)
    
    
    def printAdjacencies(self) -> None:
        for node, directlyConnected in self.adjacencyList.items():
            connectedTo = [_node.data for _node in directlyConnected]
            print(f"{node.data} -> {', '.join(connectedTo)}")

    
    def _removeConnection_unsafe(self, node1: Node, node2: Node):
        allNodes = self.adjacencyList.keys()

        if not (node1 in allNodes and node2 in allNodes):
            return
        
        self.adjacencyList.get(node1).discard(node2)
        self.adjacencyList.get(node2).discard(node1)


    def _removeNode_unsafe(self, node: Node) -> None:
        if not node in self.adjacencyList.keys():
            return

        self.adjacencyList.pop(node)
        for connections in self.adjacencyList.values():
            try:
                connections.remove(node)
            except:
                ...


    def removeConnectionAndSplit(self, node1: Node, node2: Node) -> (Self | None):
        allNodes = self.adjacencyList.keys()

        if not (node1 in allNodes and node2 in allNodes):
            return
        
        self._removeConnection_unsafe(node1, node2)

        connectedToNode2 = self.getConnectedNodes(node2)

        if node1 in connectedToNode2:
            return None
        
        newGraph = Graph(node2)
        newGraphConnections = [
            entry 
            for entry in self.adjacencyList.items()
            if entry[0] in connectedToNode2
        ]
        newGraph.adjacencyList = dict(newGraphConnections)

        self.adjacencyList.pop(node2)

        return newGraph


    
    def getConnectedNodes(self, node: Node) -> list[Node]:
        if not node in self.adjacencyList.keys():
            return []

        visitedNodes: list[Node] = [node]
        nodesToVisit: list[Node] = list(self.adjacencyList.get(node, []))

        while len(nodesToVisit) > 0:
            currentNode = nodesToVisit.pop()
            visitedNodes.append(currentNode)

            nodesToVisit.extend([
                _node 
                for _node in self.adjacencyList.get(currentNode, [])
                if not _node in visitedNodes
            ])
        
        return set(visitedNodes)