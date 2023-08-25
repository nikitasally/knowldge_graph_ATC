from py2neo import Graph

class ClearGraph:
    def __init__(self, uri, auth):
        self.graph = Graph(uri, auth=auth)

    def clear(self):
        # Delete all nodes and relationships in the graph
        query = """
        MATCH (n)
        DETACH DELETE n
        """
        self.graph.run(query)

if __name__ == "__main__":
    # Neo4j database connection details
    neo4j_uri = "bolt://localhost:7687"
    neo4j_auth = ("neo4j", "12345678")  

    # Create a ClearGraph instance
    graph_clearer = ClearGraph(neo4j_uri, neo4j_auth)

    # Clear the graph
    graph_clearer.clear()

    print("Graph cleared.")
