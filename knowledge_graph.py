from py2neo import Graph, Node, Relationship
import requests
import schedule
import time
import datetime  # Import the datetime module

#define global directories
dairports = {}
aairports = {}
fnums = {}
dates = {}
stats = {}
times = {}
airlines = {}
model_codes = {}

class BuildGraph:

    def __init__(self):
        # Connect to the Neo4j database
        self.graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))

    def createNode(self, label, properties):
        node = Node(label, **properties)
        self.graph.create(node)
        return node

    def createRelationship(self, start_node, end_node, relation_type):
        relationship = Relationship(start_node, relation_type, end_node)
        self.graph.create(relationship)

    def initialize(self, flights):

        # Helper function to add flight data to the graph
        def add_flight_to_graph(flight):
            
            flight_number = flight['flight']['icao']
            flight_iata = flight['flight']['iata']
            date = flight['flight_date']
            time = flight['departure']['estimated']
            status = flight['flight_status']
            airline = flight['airline']['name']
            arr_airport = flight['arrival']['airport']
            dep_airport = flight['departure']['airport']
            codeshared = flight['flight']['codeshared']
            
            aircraft_info = self.get_aircraft_info(flight_iata)
            
            production_line = aircraft_info['production_line']
            registration_number = aircraft_info['registration_number']
            model_code = aircraft_info['model_code']
            first_flight_date = aircraft_info ['first_flight_date']
            plane_owner = aircraft_info['plane_owner']
            plane_age = aircraft_info['plane_age']
            
            
            
            # Coerce all the values to strings
            flight_number = str(flight_number)
            date = str(date)
            time = str(time)
            status = str(status)
            airline = str(airline)
            arr_airport = str(arr_airport)
            dep_airport = str(dep_airport)
            codeshared = str(codeshared)
            production_line = str(production_line)
            registration_number = str(registration_number)
            model_code = str(model_code)
            first_flight_date = str(first_flight_date)
            plane_owner = str(plane_owner)
            plane_age = str(plane_age)

            # Check if the departure airport node already exists
            if dep_airport in dairports:
                dep_airport_node = dairports[dep_airport]
            else:
                # Create departure airport node and add it to the dictionary
                dep_airport_node = self.createNode('Departure Airport', {'name': dep_airport})
                dairports[dep_airport] = dep_airport_node

            # Check if the arrival airport node already exists
            if arr_airport in aairports:
                arr_airport_node = aairports[arr_airport]
            else:
                # Create arrival airport node and add it to the dictionary
                arr_airport_node = self.createNode('Arrival Airport', {'name': arr_airport})
                aairports[arr_airport] = arr_airport_node
                
            if flight_number in fnums:
                flight_node = fnums[flight_number]
                return
            else:
                # Create departure flight node and add it to the dictionary
                flight_node = self.createNode('Flight', {'flight_number': flight_number,
                                                         'date': date, 'time': time, 
                                                         'status': status, 
                                                         'codeshared': codeshared, 
                                                         'production_line': production_line, 
                                                         'registration_number':registration_number,
                                                         'model_code': model_code, 
                                                         'first_flight_date': first_flight_date, 
                                                         'plane_owner': plane_owner, 
                                                         'plane_age':plane_age})
                fnums[flight_number] = flight_node
                
            print(f"Flight: {flight_number} (Codeshared: {codeshared}), Departure: {dep_airport}, Arrival: {arr_airport}")


            # Check if the date node already exists
            if date in dates:
                date_node = dates[date]
            else:
                # Create date node and add it to the dictionary
                date_node = self.createNode('Date', {'date': date})
                dates[date] = date_node

            # Check if the time node already exists
            if time in times:
                time_node = times[time]
            else:
                # Create time node and add it to the dictionary
                time_node = self.createNode('Time', {'time': time})
                times[time] = time_node

            # Check if the status node already exists
            if status in stats:
                stat_node = stats[status]
            else:
                # Create status node and add it to the dictionary
                stat_node = self.createNode('Status', {'status': status})
                stats[status] = stat_node

            # Check if the airline node already exists
            if airline in airlines:
                airline_node = airlines[airline]
            else:
                # Create airline node and add it to the dictionary
                airline_node = self.createNode('Airline', {'name': airline})
                airlines[airline] = airline_node
                
            # Check if the model_code node already exists    
            if model_code in model_codes:
                model_code_node = model_codes[model_code]
            else:
                # Create departure airport node and add it to the dictionary
                model_code_node = self.createNode('Model', {'name':model_code })
                model_codes[model_code] = model_code_node
                                               

                    
            # Establish relationships between nodes
            self.createRelationship(flight_node, date_node, 'date')
            self.createRelationship(flight_node, time_node, 'time')
            self.createRelationship(flight_node, stat_node, 'status')
            self.createRelationship(flight_node, airline_node, 'operated by')
            self.createRelationship(flight_node, arr_airport_node, 'flying to')
            self.createRelationship(flight_node, dep_airport_node, 'departs from')
            self.createRelationship(flight_node, model_code_node, 'model_code')
            
            if production_line:
                production_line_node = self.createNode('Production Line', {'name': production_line})
                self.createRelationship(flight_node, production_line_node, 'production_line')

            if registration_number:
                registration_number_node = self.createNode('Registration Number', {'name': registration_number})
                self.createRelationship(flight_node, registration_number_node, 'registration_number') 

            if first_flight_date:
                first_flight_date_node = self.createNode('First Flight Date', {'name': first_flight_date})
                self.createRelationship(flight_node, first_flight_date_node, 'first_flight_date')

            if plane_owner:
                plane_owner_node = self.createNode('Plane Owner', {'name': plane_owner})
                self.createRelationship(flight_node, plane_owner_node, 'plane_owner')

            if plane_age:
                plane_age_node = self.createNode('Plane Age', {'name': plane_age})
                self.createRelationship(flight_node, plane_age_node, 'plane_age')
                
            # Recursively process codeshared flights
            if codeshared and codeshared != 'None':
                if isinstance(codeshared, list):
                    for code_flight in codeshared:
                        add_flight_to_graph(code_flight)

        # Process the initial list of flights
        for flight in flights:
            add_flight_to_graph(flight)
                                               
            
    def get_aircraft_info(self, aircraft_iata):
        url1 = f"http://api.aviationstack.com/v1/airplanes?access_key={api_key}&iata={aircraft_iata}"
        response = requests.get(url1,params=params)
        if response.status_code == 200:
            data = response.json()
            aircraft_data = data.get("data", [])
            if aircraft_data:
                return aircraft_data[0]
        return None

    
    def update_graph(self):
        # Get the current timestamp
        current_time = datetime.datetime.now()

        # Make a request to the AviationStack API to fetch flight data
        url = f"http://api.aviationstack.com/v1/flights?access_key={api_key}&dep_iata={airport_code}&limit=5"

        # Send API request
        response = requests.get(url)

        # Check response status code
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            flights = data.get("data", [])

            # Add new flights to the graph
            self.initialize(flights)

            print(f"Graph update completed at: {current_time}")
        else:
            print("Error occurred during API request.")
            print(f"Status Code: {response.status_code}")
    


if __name__ == "__main__":
    # AviationStack API endpoint and parameters
    api_key = 'a5a2a0e30d58fd1f8efbfb3e1c08c53c'
    airport_code = 'MAN'  # Manchester Airport code

    # Make a request to the AviationStack API to fetch flight data
    url = f"http://api.aviationstack.com/v1/flights?access_key={api_key}&dep_iata={airport_code}"

    # API request parameters
    params = {
        "access_key": api_key,
        "dep_iata": airport_code,
        "limit":5  # Number of flights to retrieve
    }

    # Send API request
    response = requests.get(url, params=params)

    # Check response status code
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()
        flights = data.get("data", [])

        # Create the graph
        graph_builder = BuildGraph()

        # Initialize the graph with flight data
        graph_builder.initialize(flights)

        print("Graph initialization completed.")
    else:
        print("Error occurred during API request.")
        print(f"Status Code: {response.status_code}")
        
    # Schedule the graph update to run every 5 minutes
    schedule.every(5).minutes.do(graph_builder.update_graph)

    while True:
        schedule.run_pending()
        time.sleep(1)
