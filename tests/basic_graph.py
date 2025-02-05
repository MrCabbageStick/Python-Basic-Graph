from tests.test import Test
from src.graph import Graph

@Test.test
def twoEdgeCreation() -> bool:
    graph, ANode = Graph.createAround("A")
    successful, BNode = graph.addConnected("B", ANode)

    correct_structure = graph.adjacencyList == {ANode: set([BNode]), BNode: set([ANode])}

    return successful and correct_structure

@Test.test
def edgeBetweenExistingNodes() -> bool:
    graph, ANode = Graph.createAround("A")
    BNode = graph.addNode("B")
    graph.connectNodes(ANode, BNode)

    correct_structure = graph.adjacencyList == {ANode: set([BNode]), BNode: set([ANode])}
    return correct_structure


@Test.test
def threeEdgeCreation() -> bool:
    graph, ANode = Graph.createAround("A")
    successfulB, BNode = graph.addConnected("B", ANode)
    successfulC, CNode = graph.addConnected("C", BNode)

    correct_structure = graph.adjacencyList == {ANode: set([BNode]), BNode: set([ANode, CNode]), CNode: set([BNode])}

    return successfulB and successfulC and correct_structure


@Test.test
def loopFourNodes() -> bool:
    graph, ANode = Graph.createAround("A")
    successfulB, BNode = graph.addConnected("B", ANode)
    successfulC, CNode = graph.addConnected("C", ANode)

    successfulD, DNode = graph.addConnected("D", BNode)
    graph.connectNodes(DNode, CNode)

    correct_structure = graph.adjacencyList == {
        ANode: set([BNode, CNode]), 
        BNode: set([ANode, DNode]), 
        CNode: set([ANode, DNode]),
        DNode: set([BNode, CNode])
    }

    return successfulB and successfulC and successfulD and correct_structure


@Test.test
def connectedNodes() -> bool:
    graph, ANode = Graph.createAround("A")
    successfulB, BNode = graph.addConnected("B", ANode)
    successfulC, CNode = graph.addConnected("C", ANode)

    successfulD, DNode = graph.addConnected("D", BNode)
    graph.connectNodes(DNode, CNode)
    
    return graph.getConnectedNodes(ANode) == set([ANode, BNode, CNode, DNode])


@Test.test
def removeEdgeUnsafe() -> bool:
    graph, ANode = Graph.createAround("A")
    successfulB, BNode = graph.addConnected("B", ANode)

    graph._removeConnection_unsafe(ANode, BNode)

    correctStructure = graph.adjacencyList == {ANode: set(), BNode: set()}
    return correctStructure


@Test.test
def removeNodeUnsafe() -> bool:
    graph, ANode = Graph.createAround("A")
    successfulB, BNode = graph.addConnected("B", ANode)

    graph._removeNode_unsafe(BNode)

    correctStructure = graph.adjacencyList == {ANode: set()}
    return correctStructure


@Test.test
def removeEdge() -> bool:
    graph1, ANode = Graph.createAround("A")
    successfulB, BNode = graph1.addConnected("B", ANode)

    graph2 = graph1.removeConnectionAndSplit(ANode, BNode)

    correctStructure = graph1.adjacencyList == {ANode: set()}\
                        and graph2.adjacencyList == {BNode: set()}
    
    return correctStructure


if __name__ == "__name__":
    Test.runAll()