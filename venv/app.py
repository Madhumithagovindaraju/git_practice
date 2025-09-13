# from flask import Flask, request, jsonify

# app = Flask(__name__)

# # POST API to demonstrate headers and payload
# @app.route("/api/data", methods=["POST"])
# def receive_data():
#     # Extract headers
#     headers = request.headers
#     client_token = headers.get("Authorization")  # Example header
    
#     # Extract JSON payload (body)
#     payload = request.get_json()
    
#     response = {
#         "message": "Data received successfully",
#         "received_headers": {
#             "Authorization": client_token,
#             "Content-Type": headers.get("Content-Type")
#         },
#         "received_payload": payload
#     }
    
#     return jsonify(response),200

# if __name__ == "__main__":
#     app.run(debug=True)
# =========================================

# from flask import Flask, request, jsonify
# import mysql.connector

# app = Flask(__name__)

# # Database connection
# def get_db_connection():
#     conn = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="Madhumit09*",
#         database="madhumitha"
#     )
#     return conn

# @app.route("/users", methods=["GET"])
# def get_users():
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM users")
#     rows = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return jsonify(rows)

# @app.route("/users", methods=["POST"])
# def add_user():
#     data = request.get_json()
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", 
#                    (data["name"], data["email"]))
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return jsonify({"message": "User added successfully!"}), 201

# if __name__ == "__main__":
#     app.run(debug=True)

# from flask import Flask, request, jsonify
# from db import get_db_connection

# app = Flask(__name__)

# # Add Author
# @app.route('/authors', methods=['POST'])
# def add_author():
#     data = request.get_json()
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO authors (name, country) VALUES (%s, %s)", 
#                    (data['name'], data['country']))
#     conn.commit()
#     author_id = cursor.lastrowid
#     cursor.close()
#     conn.close()
#     return jsonify({"message": "Author added", "author_id": author_id}), 201


# # Add Book
# @app.route('/books', methods=['POST'])
# def add_book():
#     data = request.get_json()
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO books (title, author_id) VALUES (%s, %s)", 
#                    (data['title'], data['author_id']))
#     conn.commit()
#     book_id = cursor.lastrowid
#     cursor.close()
#     conn.close()
#     return jsonify({"message": "Book added", "book_id": book_id}), 201


# # Get Books with Authors
# @app.route('/books', methods=['GET'])
# def get_books():
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     query = """
#         SELECT books.id, books.title, authors.name as author, authors.country
#         FROM books
#         JOIN authors ON books.author_id = authors.id
#     """
#     cursor.execute(query)
#     books = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return jsonify(books)


# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify
from redis_client import redis_client
from db import get_db_connection

app = Flask(__name__)

# Route: Insert data
@app.route("/data", methods=["POST"])
def add_data():
    data = request.json
    user_id = data.get("user_id")
    value = data.get("value")

    if not user_id or not value:
        return jsonify({"error": "user_id and value required"}), 400

    # Store in Redis (latest value)
    redis_client.set(f"user:{user_id}", value)

    # Append in Redis list (for history tracking)
    redis_client.lpush(f"user:{user_id}:history", value)

    # Store in MySQL permanently
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user_data (user_id, value) VALUES (%s, %s)",
        (user_id, value)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"msg": "Data stored in Redis & MySQL"}), 201


# Route: Get latest data from Redis
@app.route("/data/<user_id>", methods=["GET"])
def get_latest(user_id):
    value = redis_client.get(f"user:{user_id}")
    return jsonify({"user_id": user_id, "latest_value": value})


# Route: Get history from MySQL
@app.route("/data/history/<user_id>", methods=["GET"])
def get_history(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()   # No dictionary=True needed
    cursor.execute("SELECT * FROM user_data WHERE user_id=%s", (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)



if __name__ == "__main__":
    app.run(debug=True)


