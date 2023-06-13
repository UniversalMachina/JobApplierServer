# Set up the questions and possible answers
questions = [
    {
        "question": "What is the capital of France?",
        "answers": ["Paris", "Berlin", "Rome"],
        "correct": "Paris"
    },
    {
        "question": "Who developed the theory of relativity?",
        "answers": ["Isaac Newton", "Albert Einstein", "Nikola Tesla"],
        "correct": "Albert Einstein"
    },
    {
        "question": "Which language is used for web development?",
        "answers": ["Java", "Python", "JavaScript"],
        "correct": "JavaScript"
    }
]

# Function to ask a question and get the user's answer
def ask_question(question):
    print(question["question"])
    for i, answer in enumerate(question["answers"]):
        print(f"{i+1}. {answer}")
    user_answer = input("Please enter the number of your answer: ")
    return question["answers"][int(user_answer) - 1] == question["correct"]

# Iterate over the questions and ask each one
for question in questions:
    if ask_question(question):
        print("Correct!")
    else:
        print("Incorrect, the correct answer was " + question["correct"])
