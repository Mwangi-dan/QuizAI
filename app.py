from menu import *
from user import *
from database import register_new_user

def main():
    while True:
        print("\t*********************************")
        print("\t\tWelcome to QuizAI!")
        print("Please select an option:")
        print("1. Login")
        print("2. Register")
        print("3. Take a quiz (without logging in)")
        print("4. Exit")
        choice = input("Please enter your choice: ")
        try:
            choice = int(choice)
            assert choice >= 1 and choice <= 3
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
        except AssertionError:
            print("Invalid input. Please enter a number between 1 and 3.")

    if choice == 1:
        user = login_user()

        while True:
            print("Please select an option:")
            print("1. Take a quiz")
            print("2. Delete profile")
            print("3. Reset password")
            print("4. Logout")
            choice = input("Please enter your choice: ")
            try:
                choice = int(choice)
                assert choice >= 1 and choice <= 4
                break
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
            except AssertionError:
                print("Invalid input. Please enter a number between 1 and 4.")
            
        if choice == 1:
            instructions()
            gameplay()


    elif choice == 2:
        username, email, pwd = register_user()
        try:
            assert register_new_user(username, email, pwd)
            print("Registration successful!")
        except AssertionError:
            print("Registration failed. Please try again.")


    elif choice == 3:
        instructions()
        gameplay()

    else:
        print("Thank you for using QuizAI!")
        exit()



if __name__ == "__main__":
    main()