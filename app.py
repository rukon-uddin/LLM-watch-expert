from flask import Flask, render_template, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from components.dbOps import *
import requests

app = Flask(__name__)

@app.route('/')
def index():
    watches = get_data("watches")
    return render_template('index.html', watches=watches)

@app.route('/watch/<int:watch_id>')
def watch_detail(watch_id):
    conn = connect_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute("SELECT * FROM watches WHERE id = %s", (watch_id,))
        watch = cur.fetchone()
        
        cur.execute("SELECT * FROM review WHERE watch_id = %s", (watch_id,))
        reviews = cur.fetchall()
        if watch:
            return render_template('watch_detail.html', watch=watch, reviews = reviews)
        else:
            return "Watch not found", 404
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error fetching data", 500
    finally:
        cur.close()
        conn.close()


@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    title = request.json.get('title')
    price = request.json.get('price')
    description = request.json.get('description')
    instruction = f"This are the watch details. {title}. The price of the watch is {price}. The details of the watch is Description: {description}"

    response = get_chatbot_response(instruction, user_input)  # Implement this function to call your endpoint
    return jsonify({'response': response})


def get_chatbot_response(instruction, message):
    # Define the API endpoint
    url = "http://127.0.0.1:5001/generate"

    # Prepare the data to send in the POST request
    data = {
        "instruction": instruction,
        "input": message
    }

    # Make the POST request to the API
    response = requests.post(url, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        result = response.json()
        print("API Response:", result['response'])
    else:
        print("Error:", response.status_code, response.text)
    return result['response'] 

# @app.route('/api/watches')
# def api_watches():
#     watches = get_data("watches")
#     return jsonify(watches)


@app.route('/api/watches')
def api_watches():
    query = request.args.get('query', '')
    min_price = request.args.get('min_price', None)
    max_price = request.args.get('max_price', None)
    min_rating = request.args.get('min_rating', None)
    sort = request.args.get('sort', 'price_asc')

    conn = connect_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Base SQL query
        sql = "SELECT * FROM watches WHERE 1=1"
        params = []

        # Apply search query
        if query:
            sql += " AND title ILIKE %s"
            params.append(f"%{query}%")

        # Apply price filters
        if min_price:
            sql += " AND price >= %s"
            params.append(min_price)
        if max_price:
            sql += " AND price <= %s"
            params.append(max_price)

        # Apply rating filter
        if min_rating:
            sql += " AND rating >= %s"
            params.append(min_rating)

        # Apply sorting
        if sort == 'price_asc':
            sql += " ORDER BY price ASC"
        elif sort == 'price_desc':
            sql += " ORDER BY price DESC"
        elif sort == 'rating_desc':
            sql += " ORDER BY rating DESC"
        elif sort == 'rating_asc':
            sql += " ORDER BY rating ASC"

        cur.execute(sql, params)
        watches = cur.fetchall()
        return jsonify(watches)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify([]), 500
    finally:
        cur.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
