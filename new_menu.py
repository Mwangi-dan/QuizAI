import random
import openai
import key
from database import connect

openai.api_key = key.api_key
def generate_question(topic, level, num_questions=5):
    """
    Generates a set of question using the OpenAI API.
    
    :param topic: The topic the user wants to be quizzed on.
    :param level: The difficulty level the user wants to be quizzed on.

    :error: Raises an error if the API call fails.

    :return: A list of dictionaries of questions and answers.

    """
    try:
        prompt = f"Generate {num_questions} questions in the {level} difficulty level about {topic} as a 4 multiple choice question with the correct answer always the first option."

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=800,
            n=1,
            stop=None,
            temperature=0
        )

        response = response.choices[0].text.strip()

        """
        response_split = response.split("\n\n")
        que_list = []
        for i in range(len(response_split)):
            que_list.append(response_split[i].split("\n"))
            print()
        """
        # Condensed version of the code above:
        que_list = [x.split("\n") for x in response.split("\n\n")]

        # Converting the list of lists to a list of dictionaries
        converted_list = []
        for i in que_list:
            question = i[0][3:] # [3:] to remove the number from the question
            answers = [s[3:] for s in i[1:]] # [3:] to remove the letters from the answers
            correct_answer = answers[0] # stores the first answer since it's always gonna be the right answer
            que_dict = {"question": question, "answers": answers, "correct_answer": correct_answer}
            converted_list.append(que_dict)




        return converted_list
    
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return None


def display_qns(qns_list):
    """
    This function arranges the questions and answers in a random fashion for the user to answer

    :param qns_list: A list of dictionaries with the question and answers

    :error:
        - Raises an error if the user enters an invalid input

    :return: Score of the user
    """
    score = 0 # To score the score of the user
    num = 0 # To index the questions

    for qn in qns_list:
        num += 1
        random.shuffle(qn["answers"]) # shuffles the answers in random order
        print(f'Question {num}: {qn["question"]}')
        for i in range(len(qn["answers"])):
            print(f"{chr(65+i)}. {qn['answers'][i]}")
        
        # Get users answers
        while True:
            try:
                user_answer = input("Enter your answer (A, B, C, or D): ")
                assert user_answer.upper() in ["A", "B", "C", "D"]
                break
            except AssertionError:
                print("Invalid input. Please enter a valid answer (A, B, C, or D): ")
            except ValueError:
                print("Invalid input. Please enter a valid answer (A, B, C, or D): ")

        # Check if the answer is correct
        if qn["answers"][ord(user_answer.upper())-65] == qn["correct_answer"]:
            print("Correct!")
            score += 1
            print()
        else:
            print("Wrong!")
            print(f"The correct answer is: {qn['correct_answer']}")
            print()

    print(f"Your score is: {score}/{len(qns_list)}")
    score_percent = score/len(qns_list) * 100
    print()
    

    return score_percent



def user_menu():
    """
    The menu for the user to select the topic, difficulty level and number of question of the quiz

    :error:
        - Raises an error if the user enters an invalid input

    :return: A dictionary of the user's selected options

    """
    print("\t\t*** Welcome to QuizAI ***")
    
    while True:
        try:
            opt = input("1. Play Game\n2. Exit\nChoose: ")
            assert opt in ["1", "2"]
            break
        except AssertionError:
            print("Invalid input. Please enter a valid option (1 or 2): ")


    if opt == "1":
        while True:
            try:
                topic = input("Enter the topic you want to be quizzed on: ")
                assert len(topic) > 0
                break
            except AssertionError:
                print("Invalid input. Please enter a valid topic: ")

        while True:
            try:
                level = input("Enter the difficulty level you want to be quizzed on (easy, medium, or hard): ").lower()
                assert level in ["easy", "medium", "hard"]
                break
            except AssertionError:
                print("Invalid input. Please enter a valid difficulty level (easy, medium, or hard): ")

        while True:
            try:
                num_questions = int(input("Enter the number of questions you want to be quizzed on (1 - 5): "))
                assert num_questions > 0 and num_questions < 6
                break
            except AssertionError:
                print("Invalid input. Please enter a valid number of questions (1 - 5): ")
            except ValueError:
                print("Invalid input. Please enter a valid number of questions (1 - 5): ")

        return {"topic": topic, "level": level, "num_questions": num_questions}

    
    else:
        print("Goodbye!")
        exit()



def save_questions(qns_list, topic, difficulty):
    """
    Saves the questions generated into a database

    :param qns_list: A list of dictionaries with the question and answers
    :param topic: The topic of the questions
    :param difficulty: The difficulty level of the questions

    :error:
        - Raises an error if the database connection fails

    """
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                # Store the topic, questions, answers and correct_answer into the database

                # Insert the topic into the database
                topic_query = "INSERT INTO topic (topic_name, difficulty) VALUES (%s, %s)"
                topic_values = (topic), (difficulty)
                cursor.execute(topic_query, topic_values)

                topic_id = cursor.lastrowid # Get the id of the topic inserted


                for qn in qns_list:
                    qns_query = "INSERT INTO question_answers (question, correct_answer, topic_id) VALUES (%s, %s, %s)"
                    qns_values = (qn["question"]), (qn["correct_answer"]), topic_id
                    cursor.execute(qns_query, qns_values)

                
                conn.commit()
                conn.close()

    except Exception as e:
        print(f"Unexpected error occurred: {e}")



def offline():
    """
    Function is called when OpenAI cnnot be reached and accesses the database to play game with questions available there

    """
    print("Oops. It seems you're offline")
    print("Don't worry! You can still learn from previous gameplays")
    print("Select one from the listed topics:")

    with connect() as conn:
        with conn.cursor() as cursor:
            topic_query = "SELECT topic_name, difficulty FROM topic"
            cursor.execute(topic_query)
            topics = cursor.fetchall()

    num=0
    print("   TOPIC\t\tLEVEL")
    for topic in topics:
        print(f"{num+1}. ", end="")
        for i in topic:
            print(f"{i.capitalize()}", end="\t\t")
        print()


    choice = int(input("Select a topic: "))

    user_topic = topics[choice-1][0]

    with connect() as conn:
        with conn.cursor() as cursor:
            topic_query = "SELECT question, correct_answer FROM question_answers WHERE topic_id = %s"
            cursor.execute(topic_query, (choice,))
            questions = cursor.fetchall()

        conn.close()

    return questions
            

def offline_gameplay(qns_list):
    """
    Menu for the offline study

    """
    print("Attempt this questions for practice")
    question_dict = []
    for qn in qns_list:
        question_dict.append({"question": qn[0], "answer": qn[1]})


    for question in question_dict:
        print(question["question"])
        user_answer = input("Your answer: ")
        print(f"Right answer: {question['answer']}")
        print()

    

if __name__ == "__main__":
    """
    Main executed function

    """
    try:
        user_opt_dict = user_menu()
        print("Loading ...")
        questions_dict = generate_question(user_opt_dict["topic"], user_opt_dict["level"], user_opt_dict["num_questions"])
        score = display_qns(questions_dict)
        print(f"You have {score}%")
    except Exception as e:
        print(f"Unexpected error: {e}")



    


  

        

