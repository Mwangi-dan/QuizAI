import mysql.connector


# Create a function that connnects to the database of quiz_ai

def connect():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            database="quiz_ai",
            user="root"
            # password="root"
        )
        if connection.is_connected():
            return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL database: {e}")


# Create a function that adds a new user to the database
def register_new_user(username, email, password):
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user is not None:
                raise ValueError("Email already exists and is in use. Please try again.")
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
            connection.commit()
            # Return the ID of the newly inserted user
            return cursor.lastrowid
            
   
# Create a function that checks if the user exists in the database
def check_user(email, password):
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
            user = cursor.fetchone()
            return user
            

# Create a function to check whether the email exists in the database
def check_email(email):
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            return user
        

# Create a function to delete profile of user from the database
def delete_profile(email):
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE email = %s", (email,))
            connection.commit()
    
    return f"Profile for {email} has been deleted."
            

# Create a function to update the password of a user
def update_password(email, password):
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE users SET password = %s WHERE email = %s", (password, email))
            connection.commit()
    
    return f"Password for {email} has been updated."