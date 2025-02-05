from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class Node:
    data: any


class Graph:
    adjacencyList: dict[Node, list[Node]] = {}

    def __init__(self, data: any):
        self.adjacencyList = {Node(data): []}

    @classmethod
    def createAround(cls, data: any) -> tuple[Self, Node]:
        graph = cls(data)
        first_node = list(graph.adjacencyList.keys())[0]
        return (graph, first_node)
    
    def addNode(self, data: any) -> Node:
        node = Node(data)
        self.adjacencyList[node] = []
        return node
    
    def connectNodes(self, node1: Node, node2: Node) -> bool:
        allNodes = self.adjacencyList.keys()

        if not (node1 in allNodes and node1 in allNodes):
            return False
        
        self.adjacencyList[node1].append(node2)
        self.adjacencyList[node2].append(node1)

    def addConnected(self, data: any, to: Node) -> tuple[bool, Node | None]:
        if not to in self.adjacencyList.keys():
            return (False, None)
        
        node = Node(data)
        self.adjacencyList[node] = [to]
        self.adjacencyList[to].append(node)

        return (True, node)
    
    def printAdjacencies(self) -> None:
        for node, directlyConnected in self.adjacencyList.items():
            connectedTo = [_node.data for _node in directlyConnected]
            print(f"{node.data} -> {', '.join(connectedTo)}")
        
    

