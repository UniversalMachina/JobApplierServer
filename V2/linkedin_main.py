import openai
import time
import re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


openai.api_key ="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"
with open('resume_e.txt', 'r', encoding='utf-8') as file:
    resume = file.read()
with open('cover_letter_e.txt', 'r', encoding='utf-8') as file:
    cover_letter = file.read()
# print(cover_letter)

messages = []


import concurrent.futures
import openai
import time

race="asian\n"
gender='male\n'
name="Eric Dekryger"


def api_call(prompt):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt},
        ]
    )


def generate_text(prompt):
    max_attempts = 5
    for attempt in range(max_attempts):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(api_call, prompt)
            try:
                completion = future.result(timeout=120)  # timeout after 120 seconds
                return completion["choices"][0]["message"]["content"]
            except concurrent.futures.TimeoutError:
                print("Timeout occurred, retrying...")
            except Exception as e:
                print(f"Error occurred: {e}. Retrying...")
            time.sleep(1)
    print(f"Failed after {max_attempts} attempts.")



@app.route('/ask_mcq', methods=['POST'])
def ask_mcq():
    data = request.get_json()
    print(data)
    print(data['question'])
    print(data['answer'])

    # formatted_answers = '\n'.join(f"{i + 1}. {ans}" for i, ans in enumerate(question['answers']))

    user_answer = generate_text(
        f"Answer these questions from the pov of the ideal candidate with a high skill level for a job living in Canada"
        f"here is the question:\n{data['question']}\n"
        f"here are the answers:\n{data['answer']}\n"
        f"The answer should be in this format. A number, followed by the answer. Like this:\n1. The Correct Answer\n"
        f"Only return one possible answer"
    )

    # Check if answer is integer, if not request a number again
    try:
        user_answer = int(user_answer)
    except ValueError:
        user_answer = generate_text(f"The following answer will have a number followed by an answer. i.e (2. Berlin), return only the number for the answer. Only answer with the number and say nothing else:\n{user_answer}.")
        user_answer = re.sub('\D', '', user_answer)
        try:
            user_answer = int(user_answer)
        except:
            if not user_answer or user_answer < 1 or user_answer > 9:
                user_answer = 1
    print(user_answer)
    if not user_answer or user_answer < 1 or user_answer > 9:
        user_answer=1
    return jsonify({'value': int(user_answer) - 1}), 200

def check_words(input_string):
    lower_string = input_string.lower()  # Convert input string to lowercase

    if 'years' in lower_string and 'experience' in lower_string:
        return True
    elif 'gpa'  in lower_string:
        return True
    else:
        return False

# Test the function
def ask_number_question():
    question = request.get_json()
    print(question)
    print(question['question'])


    user_answer = generate_text(
        f"Here is the resume:\n {resume}\n"
        f"here is the question or information that is being inquired:\n {question['question']}\n"
        f"Answer this questions from the POV of {name}. If the resume does not have the relevant information or experience make up an answer. You do not require a visa. Assume they are knowledgeable and have a experience in most things. Return only a number answer to the question and nothing else. \n1\nis a valid answer\n1 . Fluent in English\nis an invalid answer")
    print(user_answer)

    user_answer = re.sub('[^0-9]', '', user_answer)

    # If user_answer is now an empty string, set it to '0'
    if not user_answer:
        user_answer = '0'

    # Convert user_answer to an integer
    user_answer = int(user_answer)
    # Example usage

    return user_answer

@app.route('/ask_question', methods=['POST'])
def ask_question():
    question = request.get_json()
    print(question)
    print(question['question'])
    messages.append({"role": "user", "content": question['question']})
    if len(messages) > 10:
        messages.pop(0)
    def text_gen(question):
        global resume
        global cover_letter  # assuming you have read this in from a file
    # check if 'cover letter' is in the question
        if 'cover letter' in question['question'].lower():
            user_answer = cover_letter
        elif 'reference' in question['question'].lower():
            user_answer = "-"

        elif 'twitter' in question['question'].lower():
            user_answer = "prefer not to answer"
            print(user_answer)
        elif 'portfolio' in question['question'].lower():
            user_answer = "website: https://erics-portfolio-09cd9b.webflow.io/"
            print(user_answer)
        elif check_words(question['question']):
            user_answer=ask_number_question()
        elif 'experience' in question['question'].lower():
            user_answer = generate_text(
                f"Here is the resume:\n {resume}\nrace{race}gender{gender}"
                f"Here is the question or information that is being inquired:\n {question['question']}\n"
                f"Answer this question from the POV of {name}. If the resume does not have the relevant information or experience make up an answer. Assume they they have a little experience in everything. Keep the answer as short and concise as possible\n")
            print(user_answer)
        else:
            option_picker = generate_text(f"Does this question or what is being inquired: \n{question['question']}\n Ask more about Information about the candidate such as location, salary, and Social Media OR Opinions from the candidate.\nReturn 1 for the first and 2 for the second. You must always return 1 or 2. The answer MUST only be a 1 or 2. Only return the number like this:\n1\nor\n2")
            option_picker = re.sub('[^0-9]', '', option_picker)
            if not option_picker:  # If option_picker is an empty string
                option_picker = '1'
            option_picker = int(option_picker)
            if option_picker not in [1, 2]:
                option_picker = 1
            print(f"option picked {option_picker}\n")
            if option_picker == 1:
                user_answer = generate_text(
                    f"Here is the resume:\n {resume}\nrace{race}gender{gender}"
                    f"Here is the question or information that is being inquired:\n {question['question']}\n"
                    f"Answer this question from the POV of {name}. If the resume does not have the relevant information or experience make up an answer. For personal information such as a zip code/street address OR salary expectations OR social media(Linkedin or Twitter) that's not included respond prefer not to answer. Keep the answer as short and concise as possible\n")
                print(user_answer)
            elif option_picker == 2:
                user_answer = generate_text(
                    f"Here is the resume:\n {resume}\nrace{race}gender{gender}"
                    f"Here is the question or information that is being inquired:\n {question['question']}\n"
                    f"Answer this question from the POV of {name}. If the resume does not have the relevant information make something up. Keep the answer short and concise. Do not use hashtags\n")
                print(user_answer)
            else:
                return text_gen(question)

        def remove_phrase(s, phrase):
            return s.replace(phrase, '')
        # Example usage
        user_answer=str(remove_phrase(user_answer, f'As {name}, '))
        user_answer = str(remove_phrase(user_answer, f'POV of {name}, '))
        return user_answer
    user_answer= text_gen(question)
    print(user_answer)
    messages.append({"role": "assistant", "content": user_answer})
    if len(messages) > 10:
        messages.pop(0)
    return jsonify({'message': user_answer}), 200







if __name__ == "__main__":
    app.run(port=5000)