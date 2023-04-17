import mysql.connector
from key import host, database, user, password

# Create a function that connnects to the database of quiz_ai

def connect(host, database, user, password):
    try:
        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        if connection.is_connected():
            return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL database: {e}")

