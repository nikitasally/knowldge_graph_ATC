# knowldge_graph_ATC
Neo4j Knowledge Graph Utilities offers tools for creating, managing, and visualizing Neo4j graph databases. Seamlessly interact with graph data: clear nodes, build comprehensive knowledge graphs, and use an intuitive web interface for querying. Ideal for users seeking to harness the power of Neo4j effortlessly.
Neo4j Knowledge Graph Utilities
## Overview
In the modern digital landscape, making sense of complex data relationships is vital. Graph databases, owing to their innate ability to represent and analyze sophisticated systems, are gaining prominence. Neo4j, as a leading graph database platform, is at the forefront of this revolution.
The Neo4j Knowledge Graph Utilities project encapsulates a suite of tools to help users effectively interact with their Neo4j databases. It's crafted for both technical and non-technical users to visualize, interact, and manage their graph databases with ease.
## Project Aims:
1.	Seamless Interaction: Equip users with tools to work with Neo4j without the intricacies of its underlying architecture.
2.	Boost Productivity: Automate routine tasks, thereby enhancing efficiency.
3.	Universal Access: Make the power of graph databases accessible to all, irrespective of their technical depth.
________________________________________
## Table of Contents
1. Requirements
2. Installation
3. Usage
4. Clearing the Graph
5. Building the Knowledge Graph
6. Knowledge Graph Visualizer
________________________________________
## Requirements
	Python 3.x: The suite is Python-based and requires a 3.x version.
	Neo4j: An instance of Neo4j up and running.
	Python Libraries: The tools leverage several libraries:
	flask: For web interfaces.
	py2neo: Bridge between Python and Neo4j.
	neo4j: Official Python driver for Neo4j.
________________________________________
## Installation
1.	Clone the Repository: Obtain a local copy using your preferred Git tool.
2.	Navigate: Change your directory to the cloned location.
3.	Install Dependencies: Get all required Python libraries. A virtual environment can help avoid any conflicts.
________________________________________
## Usage
### Clearing the Graph
Starting afresh is often needed. The clear_graph tool facilitates this.
1.	Set Up: Open clear_graph.py. Make sure the Neo4j database connection details match your setup.
2.	Run: Execute the script. It'll erase all nodes and relationships.
### Building the Knowledge Graph
To populate your Neo4j instance with meaningful data, use the knowledge graph utility.
1.	Preparation: Make sure your data source is accessible and formatted appropriately.
2.	Run: Kickstart the process with the knowledge_graph.py script. It will ingest the data and construct the graph in your Neo4j instance.
### Knowledge Graph Visualizer
Engage with your graph data through an intuitive web interface.
1.	Initiate: Launch the utility using the knowledge_graph_visualizer.py script.
2.	Access: Point your browser to http://localhost:8000.
3.	Interact: The interface is powered by Cypher queries. Here's how to navigate:
   
 	i)Enter your Cypher query in the textbox.

 	ii)Hit "Execute Query".

	iii)View results in a user-friendly card format, detailing attributes for easy comprehension.

Dive deep, explore relationships, or get a birds-eye view – this visualizer is your passport to the Neo4j world.
## Additional References
1.	Neo4j Installation: If you need assistance setting up Neo4j, their official GitHub repository provides comprehensive documentation. Refer here for Neo4j installation and setup.
2.	AviationStack API: The Knowledge Graph utility leverages data from the aviationstack API. Please note that you will require an API key and password for this service.


