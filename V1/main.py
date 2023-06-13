import openai
import pdfplumber
import json
from tkinter import Tk
from tkinter import filedialog

openai.api_key ="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"

def load_file(file_path):
    if file_path.endswith('.pdf'):
        with pdfplumber.open(file_path) as pdf:
            return '\n'.join([page.extract_text() for page in pdf.pages])
    elif file_path.endswith('.txt'):
        with open(file_path, 'r') as txt_file:
            return txt_file.read()
    elif file_path.endswith('.json'):
        with open(file_path, 'r') as json_file:
            return json.load(json_file)
    else:
        raise Exception("Unsupported file type")

def generate_text(prompt):
    import time
    max_attempts = 5

    for attempt in range(max_attempts):
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt},
                ]
            )
            message = completion["choices"][0]["message"]["content"]
            return message
        except Exception as e:
            print(f"Error occurred: {e}. Retrying...")
            time.sleep(1)
    else:
        print(f"Failed after {max_attempts} attempts.")

def select_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

def open_ai_request():
    file_path = select_file()
    resume = load_file(file_path)

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
    questions = [
        {
            "question": "Do you have a GED or high school diploma?",
            "answers": ["Yes", "No"],
            "correct": "Yes"
        },
        {
            "question": "Do you have any previous experience in this field?",
            "answers": ["Yes", "No"],
            "correct": "Yes"
        },
        {
            "question": "Are you legally eligible to work in this country?",
            "answers": ["Yes", "No"],
            "correct": "Yes"
        },
        {
            "question": "Are you able to work in a team environment?",
            "answers": ["Yes", "No"],
            "correct": "Yes"
        },
        {
            "question": "Do you have a valid driver's license?",
            "answers": ["Yes", "No"],
            "correct": "Yes"
        },
        {
            "question": "How many years of experience do you have in this field?",
            "answers": ["Less than 1 year", "1-3 years", "3-5 years", "More than 5 years"],
            "correct": None  # No objectively correct answer for this question
        }
    ]

    # Function to ask a question and get the user's answer
    def ask_question(question,resume):
        print(question["question"])
        for i, answer in enumerate(question["answers"]):
            print(f"{i + 1}. {answer}")
            #If the answer is not provided in the resume return an answer best you can. You must always return an answer.
        formatted_answers = '\n'.join(f"{i + 1}. {ans}" for i, ans in enumerate(question['answers']))

        user_answer = generate_text(
            f"Answer these questions from the pov of the ideal candidate for a job"
            f"here is the question:\n{question['question']}\n"
            f"here are the answers:\n{formatted_answers}\n"
            f"The answer should be in this format. A number, followed by the answer. Like this:\n1. The Correct Answer"
        )

        print(user_answer)

        try:
            int_value = int(user_answer)
        except ValueError:
            print("answer is not an int")
            user_answer = generate_text(f"The following answer will have a number followed by an answer. i.e (2. Berlin), return only the number for the answer. Only answer with the number and say nothing else:\n{user_answer}.")
            import re
            user_answer = re.sub('\D', '', user_answer)
            print(user_answer)
        # user_answer = input("Please enter the number of your answer: ")
        return question["answers"][int(user_answer) - 1] == question["correct"]

    # Iterate over the questions and ask each one
    for question in questions:
        if ask_question(question,resume):
            print("Correct!")
        else:
            print("Incorrect, the correct answer was " + question["correct"])


open_ai_request()
