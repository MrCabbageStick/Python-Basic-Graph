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
    _, BNode = graph.addConnected("B", ANode)
    _, CNode = graph.addConnected("C", ANode)

    _, DNode = graph.addConnected("D", BNode)
    graph.connectNodes(DNode, CNode)
    
    return graph.getConnectedNodes(ANode) == set([ANode, BNode, CNode, DNode])


@Test.test
def removeEdgeUnsafe() -> bool:
    graph, ANode = Graph.createAround("A")
    _, BNode = graph.addConnected("B", ANode)

    graph._removeConnection_unsafe(ANode, BNode)

    correctStructure = graph.adjacencyList == {ANode: set(), BNode: set()}
    return correctStructure


@Test.test
def removeNodeUnsafe() -> bool:
    graph, ANode = Graph.createAround("A")
    _, BNode = graph.addConnected("B", ANode)

    graph._removeNode_unsafe(BNode)

    correctStructure = graph.adjacencyList == {ANode: set()}
    return correctStructure


@Test.test
def removeEdge() -> bool:
    graph1, ANode = Graph.createAround("A")
    _, BNode = graph1.addConnected("B", ANode)

    graph2 = graph1.removeConnectionAndSplit(ANode, BNode)

    correctStructure = graph1.adjacencyList == {ANode: set()}\
                        and graph2.adjacencyList == {BNode: set()}

    return correctStructure


@Test.test
def removeNodeNoSplit() -> bool:
    graph, ANode = Graph.createAround("A")
    _, BNode = graph.addConnected("B", ANode)
    _, CNode = graph.addConnected("C", BNode)

    newGraphs = graph.removeNode(CNode)

    correctStructure = len(newGraphs) == 0 \
                        and graph.adjacencyList == {ANode: set([BNode]), BNode: set([ANode])}
    
    return correctStructure


@Test.test
def removeNodeWithSplit() -> bool:
    """
    Graph:
            D - E
            |
        A - B - C
    
    Should split into:
    A, C, D-E
    """
    graph, ANode = Graph.createAround("A")
    _, BNode = graph.addConnected("B", ANode)
    _, CNode = graph.addConnected("C", BNode)
    _, DNode = graph.addConnected("D", BNode)
    _, ENode = graph.addConnected("E", DNode)

    newGraphs = graph.removeNode(BNode)

    correctStructure = True

    for _graph in newGraphs.union([graph]):
        if not correctStructure:
            break

        nodes = _graph.adjacencyList.keys()

        if ANode in nodes:
            correctStructure = _graph.adjacencyList == {ANode: set()}
        elif BNode in nodes:
            correctStructure = False
        elif CNode in nodes:
            correctStructure = _graph.adjacencyList == {CNode: set()}
        elif DNode in nodes:
            correctStructure = _graph.adjacencyList == {DNode: set([ENode]), ENode: set([DNode])}

    return correctStructure


if __name__ == "__name__":
    Test.runAll()
