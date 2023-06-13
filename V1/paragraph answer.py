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
    print("starting")
    # Set up the questions and possible answers


    # Function to ask a question and get the user's answer
    def ask_question(question,resume):


        user_answer = generate_text(
            f"Here is the resume:\n {resume}\n"
            f"here is the question:\n {question}\n"
            f"Answer this questions from the POV of Eric Bennett. If the resume does not have the relevant information make up an answer. Keep the answer short and concise\n")

        print(user_answer)

        def remove_phrase(s, phrase):
            return s.replace(phrase, '')

        # Example usage
        user_answer=remove_phrase(user_answer, 'As Eric Bennett, ')

        return user_answer

    # Iterate over the questions and ask each one
    # question = "Can you please provide an example of a challenging writing project you completed and describe how you overcame the challenges"
    # print(ask_question(question,resume))
    questions = [
        "Can you please provide an example of a challenging writing project you completed and describe how you overcame the challenges?",
        "What is your greatest strength?",
        "What is your greatest weakness?",
        "Why should we hire you?",
        "Where do you see yourself in five years?"
    ]

    for question in questions:
        answer = ask_question(question, resume)
        print(f'Q: {question}\nA: {answer}\n')



open_ai_request()
