import openai
import random
import re
import time
from key import api_key as key

openai.api_key = key


def correct_spelling(input_str):
    """Corrects wrong spelling in a string using OpenAI's GPT-3 API.
    Parameters:
        input_str (str): The string to be corrected.

    Returns:
        corrected_str (str): The corrected string.

    """
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Correct the spelling in the following sentence: {input_str}\nCorrected sentence:",
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )

    corrected_str = response.choices[0].text.strip()
    return corrected_str


def menu():
    """Menu Function
    This function allows user to choose the topic they want to be quizzed on, the difficulty level, \
        and the number of questions they want to be asked.

    Parameters:
        None

    Returns:
        topic (str): The topic the user wants to be quizzed on.
        difficulty (str): The difficulty level the user wants to be quizzed on.

    """
    choices = ["easy", "medium", "hard"]

    topic = input("Please enter your desired topic: ")
    while True:
        difficulty = input("Please enter the desired difficulty level (easy, medium, or hard): ")
        try:
            assert difficulty.lower() in choices
            break
        except AssertionError:
            print("Invalid input. Please enter a valid difficulty level (easy, medium, or hard): ")
        except ValueError:
            print("Invalid input. Please enter a valid difficulty level (easy, medium, or hard): ")
    
    return topic, difficulty


def generate_questions(topic, difficulty):
    """Generate Questions Function from OpenAI GPT-3 API

    Parameters:
        topic (str): The topic the user wants to be quizzed on.
        difficulty (str): The difficulty level the user wants to be quizzed on.

    Returns:
        qa_dict (dict): A dictionary of questions and answers.

    """
    # Generate questions and answers using OpenAI API
    prompt = f"Generate a {difficulty} difficulty question about {topic}."
    generated_text = openai.Completion.create(
        engine="text-davinci-003", 
        prompt=prompt,
        max_tokens=800,
        n=1,
        stop=None,
        temperature=0.1
    )
    generated_text = generated_text.choices[0].text.strip()
    
    qa_list = generated_text.split("\n")

    qa_dict = {}

    for question in qa_list:

        # Write code that generates the correct answer and three false answers

        answer = openai.Completion.create(
            engine="text-davinci-002", 
            prompt=f"Generate the correct answer plus three false answers to the question. '{question}'",
            max_tokens=800,
            n=1,
            stop=None,
            temperature=0.4
        ).choices[0].text.strip()
        
        # Write code that splits the answers into the correct answer and the fake answers
        answer = answer.split("\n")
        # get rid of number or uppercase or lowercase letters before answer
        answer = [re.sub(r"^[0-9]\.", "", x) for x in answer]
        # Get rid of empty strings
        answer = [x for x in answer if x != ""]
        correct_answer = answer[0]
        answer_choices = answer[1:3]
        qa_dict[question] = [correct_answer] + answer_choices

    return qa_dict



def instructions():
    """
    This function prints the instructions of the game.
    """
    print("\t\tRules of the game:")
    print("\t\t------------------")
    print("1. You will be prompted to enter a topic and a difficulty level.")
    print("2. You will be given a question and 4 possible answers.")
    print("3. You will have to choose the correct answer.")
    print("4. You will be given a score at the end of the game.")
    print("5. You can choose to play again or quit the game.")
    print("\t\tGoodluck!\n")
    print("\t\t------------------")


def gameplay():
    """
    This function allows user to play the game.
    
    """
    while True:
        topic, difficulty = menu()
        i = 1
        score = 0
        while i < 5:
            qa_dict = generate_questions(topic, difficulty)
            if i == 1:
                print("Loading questions...")
                time.sleep(1)
                print("Questions loaded!")
                print("Game starts in 3...")
                time.sleep(1)
                print("2...")
                time.sleep(1)
                print("1...")
                time.sleep(1)
                print("GO!")
                time.sleep(1)
            for key, value in qa_dict.items():
                correct_answer = value[0]
                random.shuffle(value)
                correct_answer_index = value.index(correct_answer)
                print(f"{key}")
                for j in range(len(value)):
                    print(f"{chr(65+j)}. {value[j]}")
                while True:
                    try:
                        answer = input("Please enter your answer (A, B, C, or D): ")
                        assert answer.upper() in ["A", "B", "C", "D"]
                        break
                    except AssertionError:
                        print("Invalid input. Please enter a valid answer (A, B, C, or D): ")
                    except ValueError:
                        print("Invalid input. Please enter a valid answer (A, B, C, or D): ")
                if answer.upper() == chr(65+correct_answer_index):
                    print("Correct!")
                    score += 100
                else:
                    print("Incorrect!")
                print()
                i += 1
        while True:
            try:
                play_again = input("Would you like to play again? (Y/N): ")
                assert play_again.upper() in ["Y", "N"]
                break
            except AssertionError:
                print("Invalid input. Please enter a valid answer (Y/N): ")
            except ValueError:
                print("Invalid input. Please enter a valid answer (Y/N): ")
        if play_again.upper() == "N":
            break

def game_menu():
    """
    This function allows user to choose to play the game or quit the game.
    """
    print("Please select an option:")
    print("1. Take a quiz")
    print("2. Delete profile")
    print("3. Reset password")
    print("4. Logout")
    choice = input("Please enter your choice: ")

    while True:
        try:
            choice = int(input("Please enter your choice: "))
            assert choice in [1, 2, 3, 4]
            break
        except AssertionError:
            print("Invalid input. Please enter a valid choice (1 to 4): ")
        except ValueError:
            print("Invalid input. Please enter a valid choice (1 to 4): ")
    
    return choice


def space():
    print("-----------------------------\n")