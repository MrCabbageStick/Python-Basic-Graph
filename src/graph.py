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

        connectedTo = self.adjacencyList.get(node)
        self.adjacencyList.pop(node)

        for endNode in connectedTo:
            self.adjacencyList.get(endNode).discard(node)


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


    def removeNode(self, node: Node) -> set[Self]:
        if not node in self.adjacencyList.keys():
            return set()
        
        danglingNodes = self.adjacencyList.get(node)
        self._removeNode_unsafe(node)

        if len(danglingNodes) == 0:
            return set()

        # Find nodes outside of the graph
        currentGraphNodes = self.getConnectedNodes(danglingNodes.pop())
        danglingNodes = danglingNodes.difference(currentGraphNodes)

        newGraphs: set[Graph] = set()

        # Combine dangling nodes to new graphs
        while len(danglingNodes) > 0:
            newGraphSeed = danglingNodes.pop()
            newGraphNodes = self.getConnectedNodes(newGraphSeed)

            newGraph = Graph(None)
            newGraph.adjacencyList = dict([
                entry
                for entry in self.adjacencyList.items()
                if entry[0] in newGraphNodes
            ])
            newGraphs.add(newGraph)

            danglingNodes = danglingNodes.difference(newGraphNodes)

            for nodeToRemove in newGraphNodes:
                self.adjacencyList.pop(nodeToRemove)

        return newGraphs

    
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
    

    def mergeWith(self, graphNode: Node, otherGraph: Self, otherGraphNode: Node) -> None:
        if not (graphNode in self.adjacencyList.keys() and otherGraphNode in otherGraph.adjacencyList.keys()):
            return
        
        # Connect nodes
        self.adjacencyList[graphNode].add(otherGraphNode)
        otherGraph.adjacencyList[otherGraphNode].add(graphNode)
        
        # Merge adjacency lists
        self.adjacencyList.update([
            *self.adjacencyList.items(),
            *otherGraph.adjacencyList.items()
        ])

        # Make transfer more permanent
        otherGraph.adjacencyList = {}



