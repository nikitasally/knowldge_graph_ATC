from flask import Flask, render_template_string, request
from neo4j import GraphDatabase

app = Flask(__name__)

html_code = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Neo4j Flight Explorer</title>
    <style>
        /* Basic Reset */
        body, h1, h2, h3, h4, p, form {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
        }

        body {
            background-color: #f4f4f8;
            color: #333;
            font-size: 16px;
            line-height: 1.6;
            padding: 20px;
        }

        /* Header */
        h1 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #4A90E2;
        }

        /* Form Styling */
        form {
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            max-width: 500px;
            margin: 0 auto 30px;
            animation: fadeIn 0.6s forwards;
        }

        label {
            font-weight: bold;
            display: block;
            margin-bottom: 8px;
        }

        input[type="text"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }

        input[type="submit"] {
            background-color: #4A90E2;
            color: #fff;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        input[type="submit"]:hover {
            background-color: #357ABD;
        }

        /* Card Styling */
        .card {
            border: 1px solid #ddd;
            width: 250px;
            padding: 10px;
            margin: 10px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
            border-radius: 5px;
            display: inline-block;
            background: #fff;
        }

        /* Animations */
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
</head>
<body>
    <h1>Neo4j Flight Explorer</h1>
    <form action="/search" method="post">
        <label for="query">Enter your Cypher query:</label>
        <input type="text" id="query" name="query" required>
        <input type="submit" value="Execute Query">
    </form>
    {% if results %}
    <h2>Query: {{ query }}</h2>
    {% for result in results %}
    {% if result['flight_number'] %}
    <div class="card">
        <h4>Flight: {{ result['flight_number'] }}</h4>
        <p>Date: {{ result['date'] or '-' }}</p>
        <p>Time: {{ result['time'] or '-' }}</p>
        <p>Status: {{ result['status'] or '-' }}</p>
        <p>Prod. Line: {{ result['production_line'] or '-' }}</p>
        <p>Reg. No.: {{ result['registration_number'] or '-' }}</p>
        {% if result['departure_airport'] %}<p>Dep.: {{ result['departure_airport'] }}</p>{% endif %}
        {% if result['arrival_airport'] %}<p>Arr.: {{ result['arrival_airport'] }}</p>{% endif %}
        {% if result['airline'] %}<p>Airline: {{ result['airline'] }}</p>{% endif %}
        <p>Model: {{ result['model_code'] or '-' }}</p>
        <p>First Flight: {{ result['first_flight_date'] or '-' }}</p>
        <p>Owner: {{ result['plane_owner'] or '-' }}</p>
        <p>Age: {{ result['plane_age'] or '-' }} yrs</p>
    </div>
    {% endif %}
    {% endfor %}
    {% endif %}
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(html_code)

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = execute_query(query)
    return render_template_string(html_code, query=query, results=results)

def execute_query(query):
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))
    with driver.session() as session:
        results = session.run(query)
        flights = []
        for record in results:
            flight = {
                "flight_number": record['n']['flight_number'],
                "date": record['n']['date'],
                "time": record['n']['time'],
                "status": record['n']['status'],
                "production_line": record['n']['production_line'],
                "registration_number": record['n']['registration_number'],
                "departure_airport": record['n']['departure_airport'],
                "arrival_airport": record['n']['arrival_airport'],
                "airline": record['n']['airline'],
                "model_code": record['n']['model_code'],
                "first_flight_date": record['n']['first_flight_date'],
                "plane_owner": record['n']['plane_owner'],
                "plane_age": record['n']['plane_age']
            }
            flights.append(flight)
        return flights

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
