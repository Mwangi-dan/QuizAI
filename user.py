import hashlib
from database import register_new_user, check_email, check_user, connect

class User:

    user_count = 0

    def __init__(self, first_name, email, password):
        self._first_name = first_name
        self._email = email
        self._password = self._hash_password(password)
        self.scores = []
        self.topics_covered = []
        User.user_count += 1

    def add_score(self, score):
        self.scores.append(score)
    
    def add_topic(self, topic):
        self.topics_covered.append(topic)

    @property
    def get_name(self):
        return self._first_name

    @property
    def get_email(self):
        return self._email
        
    def _hash_password(self, password):
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        return hashed_password
    
    @property
    def set_password(self, password):
        self._password = self._hash_password(password)

            
    def delete_profile(self, username):
        if username == self.name:
            self.name = None
            self.password_hash = None
            User.user_count -= 1
            return f"Profile for {username} has been deleted."
        else:
            return f"No profile found for {username}."

    def check_password(self, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return password_hash == self.password_hash

    @classmethod
    def reset_password(self, new_password):
        self.password_hash = self._hash_password(new_password)
        print(f"Password reset successful for user {self.name}.")


    @staticmethod
    def check_user(email, password):
        with connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                row = cursor.fetchone()
                if row and User._hash_password(password) == row[2]:
                    return User(*row)


    def __str__(self):
        return f"{self._first_name} {self._email}"

    def __repr__(self):
        return f"User('{self._first_name}', '{self._email}')"
    


def register_user():
    """Registers a new user
    
    """
    f_name = input("Enter your first name: ")
    email = input("Enter your email: ")
    pwd = input("Enter your password: ")
    confirm_pwd = input("Confirm your password: ")

    while pwd != confirm_pwd:
        print("Passwords do not match. Please try again.")
        pwd = input("Enter your password: ")
        confirm_pwd = input("Confirm your password: ")

    confirm_pwd = hashlib.sha256(confirm_pwd.encode('utf-8')).hexdigest()
    
    return f_name, email, confirm_pwd 


def login_user():
    """Logs in a user
    
    """
    email = input("Enter your email: ")
    pwd = input("Enter your password: ")
    # hashes the password
    pwd = hashlib.sha256(pwd.encode('utf-8')).hexdigest()

    return email, pwd
