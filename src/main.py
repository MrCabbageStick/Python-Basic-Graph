from graph import Graph, Node

def main() -> None:
    graph, ANode = Graph.createAround("A")

    _, BNode = graph.addConnected("B", ANode)
    graph.addConnected("C", BNode)

    graph.printAdjacencies()


if __name__ == "__main__":
    main()