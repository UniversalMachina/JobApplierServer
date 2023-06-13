import openai
import time
import re

openai.api_key ="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"



def generate_text(prompt):
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt},
                ]
            )
            return completion["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error occurred: {e}. Retrying...")
            time.sleep(1)
    print(f"Failed after {max_attempts} attempts.")

def ask_mcq(question):
    formatted_answers = '\n'.join(f"{i + 1}. {ans}" for i, ans in enumerate(question['answers']))

    user_answer = generate_text(
        f"Answer these questions from the pov of the ideal candidate for a job"
        f"here is the question:\n{question['question']}\n"
        f"here are the answers:\n{formatted_answers}\n"
        f"The answer should be in this format. A number, followed by the answer. Like this:\n1. The Correct Answer"
    )

    # Check if answer is integer, if not request a number again
    try:
        int_value = int(user_answer)
    except ValueError:
        user_answer = generate_text(f"The following answer will have a number followed by an answer. i.e (2. Berlin), return only the number for the answer. Only answer with the number and say nothing else:\n{user_answer}.")
        user_answer = re.sub('\D', '', user_answer)
    return int(user_answer)-1

def ask_question(question,resume):

    user_answer = generate_text(
        f"Here is the resume:\n {resume}\n"
        f"here is the question:\n {question}\n"
        f"Answer this questions from the POV of Eric Bennett. If the resume does not have the relevant information make up an answer. Keep the answer short and concise\n")

    def remove_phrase(s, phrase):
        return s.replace(phrase, '')
    # Example usage
    user_answer=remove_phrase(user_answer, 'As Eric Bennett, ')

    return user_answer

def open_ai_request():
    # file_path = select_file()
    # resume = load_file(file_path)
    resume=\
        """Eric Bennett
289-682-0702 • username9037@gmail.com
Portfolio: https://drive.google.com/drive/folders/15vwnZsfWN8JQmX3BSNBP4vThkLjHcFLB?usp=sharing
SUMMARY/OBJECTIVE
Accomplished Content Strategist, Writer, Creative Writer, and Published Author with expertise in crafting diverse narratives
and technical documentation with over 8 years experience. Known for strong communication skills, technical prowess, and a
passion for storytelling. Seeking a challenging role where my skills can contribute to creating engaging, accessible content
aligned with organizational objectives.
EXPERIENCE
Senior Writer | Donmar Properties Ltd - BC, CA
June 2022 – 2023
• Crafted and optimized diverse documents, enhancing company narrative.
• Collaborated with teams for strategic content, aiding company objectives.
• Led marketing initiatives, contributing to sale of 50 properties valued at $4M+.
Freelance Writer & Content Specialist | Various Clients
January 2015 – Present
• Executed SEO and copywriting strategies, expanding digital footprint.
• Provided meticulous proofreading, ensuring content accuracy.
• Crafted versatile content, fulfilling diverse client needs.
Author | Self-Published
January 2022 – 2023
• Authored "Plumetless" series, receiving positive feedback and selling 5,000+ copies.
• View my published work here: https://plummetless.org/
Technical Writer | Khan Industrial
January 2019 – December 2020
• Composed technical articles, simplifying industrial concepts.
• Collaborated with teams to ensure content accuracy.
• Increased the company's online engagement by 20% with industry-specific content.
EDUCATION
Bachelor of Arts in English Literature, Laurentian University - Sudbury, ON
September 2018 - May 2022
CERTIFICATIONS
• Creative Writing Specialization | Wesleyan University, June 2018
• Memoir and Personal Essay: Write About Yourself Specialization | Wesleyan University, August 2019
• English Composition I | Duke University, December 2017
• Academic English: Writing Specialization | University of California, Irvine, April 2017
SKILLS/INTERESTS
English language mastery, technical writing, proficient in MS Office/Adobe/Confluence/Markdown, cross-functional
collaboration, exceptional editing/proofreading, UX writing, business plans, article writing, blogging, creative problem-solving,
critical thinking, copywriter skills, strong research skills, SEO specialization, teamwork skills."""

    # Set up the questions and possible answers
    questions = [
        {
            "question": "Do you have a GED or high school diploma?",
            "answers": ["No", "Yes"],
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

    # Iterate over the questions and ask each one
    for question in questions:
        print(ask_mcq(question))

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
