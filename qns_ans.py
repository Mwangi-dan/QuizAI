from menu import generate_questions, menu

def main():
    """Main Function
    This function allows user to choose the topic they want to be quizzed on, the difficulty level, \
        and the number of questions they want to be asked.

    Parameters:
        None

    Returns:
        None

    """
    topic, difficulty, num_questions = menu()
    questions = generate_questions(topic, difficulty, num_questions)
    for q , a in questions.items():
        print(q)
        for i, j in enumerate(a):
            print(f"{chr(65+i)}. {j}")
        print()

if __name__ == "__main__":
    main()