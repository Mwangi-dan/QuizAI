import hashlib

class User:

    user_count = 0

    def __init__(self, first_name, email, password):
        self._first_name = first_name
        self._email = email
        self._password = self._hash_password(password)
        self.scores = []
        self.topics_covered = []
        self.user_count += 1

    def add_score(self, score):
        self.scores.append(score)
    
    def add_topic(self, topic):
        self.topics_covered.append(topic)

    @property
    def get_name(self):
        return self._name
    

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
    
        
    def reset_password(self, new_password):
        self.password_hash = self._hash_password(new_password)
        print(f"Password reset successful for user {self.name}.")


    def __str__(self):
        return f"{self._first_name} {self._email}"

registered_users = {}

def register_user():
    """Registers a new user
    
    """
    f_name = input("Enter your first name: ")
    email = input("Enter your email: ")
    pwd = input("Enter your password: ")

    new_user = User(f_name, email, pwd)

    registered_users[f_name] = new_user

    print(f"Welcome {f_name}! You have been registered as a new user.")


def login_user():
    """Logs in a user
    
    """
    f_name = input("Enter your first name: ")
    email = input("Enter your email: ")
    pwd = input("Enter your password: ")

    if email in registered_users:
        user = registered_users[email]
        if user._password == user._hash_password(pwd):
            print(f"Welcome back {f_name}!")
        else:
            print("Incorrect password.")
    else:
        print("User not found.")


