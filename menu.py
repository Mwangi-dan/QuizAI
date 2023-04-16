import openai
from key import api_key as key
import spacy
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
        num_questions (int): The number of questions the user wants to be asked.

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

    while True:        
        num_questions = input("Please enter the desired number of questions (1-5): ")
        try:
            num_questions = int(num_questions)
            assert num_questions >= 1 and num_questions <= 5
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
        except AssertionError:
            print("Invalid input. Please enter a number between 1 and 5.")
    
    return topic, difficulty, num_questions


def generate_questions(topic, difficulty, num_questions=3):
    """Generate Questions Function from OpenAI GPT-3 API

    Parameters:
        topic (str): The topic the user wants to be quizzed on.
        difficulty (str): The difficulty level the user wants to be quizzed on.
        num_questions (int): The number of questions the user wants to be asked.

    Returns:
        qa_dict (dict): A dictionary of questions and answers.

    """
    # Generate questions and answers using OpenAI API
    prompt = f"Generate {num_questions} {difficulty} question and answer about {topic}"
    generated_text = openai.Completion.create(
        engine="text-davinci-002", 
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.3
    )

    # Extract questions and answers using regular expressions
    generated_text = generated_text.choices[0].text.strip()
    
    qa_list = [qa for qa in generated_text.split("\n") if qa != ""]
    qa_dict = {}

    # for i in range(0, len(qa_list) -1 , 2):
    #     question = qa_list[i]
    #     answer = qa_list[i+1]
    #     qa_dict[question] = answer

    for i in range(0, len(qa_list) -1 , 2):
        question = qa_list[i]
        answer = qa_list[i+1]
        false_answers = [
            # generate 3 false answers using OpenAI API
            openai.Completion.create(
                engine="text-davinci-002", 
                prompt=f"Generate a false answer about {topic} related to {answer}",
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.3
            ).choices[0].text.strip()
            for j in range(3)
        ]
        qa_dict[question] = [answer] + false_answers
    print(qa_dict)

    return qa_dict

que = generate_questions("python", "easy", 3)
