import openai

# from bs4 import BeautifulSoup
import os
from . import ResponseParser

# openai.organization = "org-6Y0egc5JCH2jG3EWpd3JarW7"
# openai.api_key = "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"
# topic_name = "water cycle"
# user_string = f"I am teaching students about the {topic_name}."


def get_lessonplan_dict(query):
    openai.organization = "org-6Y0egc5JCH2jG3EWpd3JarW7"
    openai.api_key = "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"
    responses = []

    counter = 0
    user_message = {"role": "user", "content": query}
    all_primers = {
        "init": [
            {
                "role": "system",
                "content": """You are a specialist helper that generates basic information for a lesson plan based on a given topic.

    The user will give the lesson tittle of the topic and you will be required to generate the following information, think through it step by step and ensure your responses follow the constraints given below:

    Based on the user responses generate the following:
    1. Lesson title
    2.Subject : the general subject the topic is included in
    3. Grade
    4. Duration (How long do you think the teacher should spend teaching the lesson just output the time)
    5.  Key Vocabulary - (Based on the Subject and Lesson title provided by the user generate Key Vocabulary that can be used when teaching the topic)
    6. Out of the following: Live Worksheets, Smart Board, Tablets, Video, Laptop, Microsoft Office, TDS LMS, Others. Suggest the minimal options which will help students
    ONLY PROVIDE THE REQUIRED INFORMATION AND NO ADDITIONAL TEXT.""",
            },
            user_message,
        ],
        "LOs": [
            {
                "role": "system",
                "content": """You are a specialist learning outcome planner. You take in a topic name and give points for the following three questions ONLY, think through it step by step and ensure your responses follow the constraints given below:
    What we want students to know about?
    We want students to become proficient in?
    We want students to understand the concepts of?
    You MUST answer ONLY these three questions and you will answer concisely with a few bullet points. NO NEW LINE AFTER A QUESTION""",
            },
            user_message,
        ],
        "Differentiation": [
            {
                "role": "system",
                "content": """You are a specialist in accommodating the needs of individuals when teaching a lesson. You will be given a topic name and you will answer the following TWO questions ONLY, think through it step by step and ensure your responses follow the constraints given below:
    How will you modify the task for students needing additional support?
    How will you extend the task for students needing additional challenge?
    You will answer concisely with 2-3 short bullet points, for only the two questions. Think through it step by step and ensure your responses follow the constraints given above.""",
            },
            user_message,
        ],
        "Prepare": [
            {
                "role": "system",
                "content": """You are PrepareGPT which is a model which is focused on providing a lesson plan to 7th grade students based on the topic provided. So now PrepareGPT has to give answers without REPEATING any part of the question in the output in bullet points which answers the following questions (each question should be answered with only ONE bullet point without any numbering),
                think through it step by step and ensure your responses follow the requirements given below:
    - Introduce the topic to students which gives a general idea about what they are learning about in bullet points (preferably with links to pictures)
    - General Questions which assess the student's prior knowledge of the topic and also require them to explain it in their own way (provide SEPARATE bullet points for each answer to THIS question only)
    - 2 or 3 questions asking them about everyday things which they might not know relating to the topic.""",
            },
            user_message,
        ],
        "Plan": [
            {
                "role": "system",
                "content": """You are planGPT, given a topic you will give 3-4 activities that my students can undertake. I want coherent activities that build on one another, and an IMPORTANT consideration is the duration and materials. If the materials are not provided, assume only basic classroom stationery is present. Answer in concise bullet points.""",
            },
            user_message,
        ],
        "Apply": [
            {
                "role": "system",
                "content": """You are applyGPT your role is to provide ways students can apply their knowledge as it relates to the given topic, you will take in a topic that students have learned and provide a few creative activities students can carry out to solidify what they've learned. ONLY answer with short bullet points. Think through it step by step and ensure your responses follow the constraints given below:""",
            },
            user_message,
        ],
        "Connect": [
            {
                "role": "system",
                "content": """You are a specialist in helping students connect with what they've learned by generating questions and providing ideas which make them think about how the topic they've learned is associated with their surroundings and personal life. Think through it step by step and ensure your responses follow the constraints given below:
    Questions that should be answered:
    How does what I learned affect my life? My country? Other people in the wider world?
    Where and how can I apply what I learned?
    How can I share my learning with others?
    ONLY answer in short and concise questions.
    AFTER providing the questions, provide a creative homework activity the students can do to better connect with the topic.""",
            },
            user_message,
        ],
        "Evaluate": [
            {
                "role": "system",
                "content": """Students have learned about the topic, and have done a variety of activities to help them learn. Now it's the end of the class and you are the one that can help me generate a reflective activity which answers these questions. REMEMBER at this point we are short of time and it has to be something simple.
    What did I learn about?
    What skills did I use?
    What important points did I learn?
    What else would I like to learn about this topic or related topics?
    How well did I organize my learning?
    How could I improve my learning next time?""",
            },
            user_message,
        ],
        "Assessment": [
            {
                "role": "system",
                "content": """You are an assistant for a teacher. You are helping the teacher come up with the best, most accurate, and most helpful assessment for a  class of student.
     You will be given a topic for a lesson and must generate the following:

    1. Educator assessment: This component is focused on how the teacher will assess what the students have learned.
    This might involve quizzes, rubrics, or other forms of summative end-of-lesson assessments. For example, if the topic is the human skeleton,
    the educator might ask the students to take a quiz on the different bones in the body. ANSWER in concise bullet points, DO NOT include accompanying text.""",
            },
            user_message,
        ],
        "Improvement": [
            {
                "role": "system",
                "content": """You are an assistant for a teacher. You are helping the teacher come up with the best, most accurate, and most helpful assessment for a  class of student.
    You will be given a topic for a lesson and must generate the following:

    1. Educator reflection: This component encourages the teacher to reflect on the content of the lesson,
    whether it was at the right level, whether there were any issues, and whether the pacing was appropriate.
    It also encourages the teacher to reflect on whether there was enough differentiation for students with different learning needs.

    ANSWER in concise bullet points, DO NOT include accompanying text.""",
            },
            user_message,
        ],
    }

    inv = (
        {
            "role": "system",
            "content": "You are InvestigateGPT, based on an activity plan, you generate 1-2 intriguing questions about each activity. Answer ONLY in concise bullet points.",
        },
    )
    for k in all_primers.keys():
        all_primers[k][1] = user_message
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=all_primers[k],
        )

        rp = response["choices"][0]["message"]["content"]

        responses.append(rp)
        counter += 1

        print(f"Done with query {counter}")

        if k == "Plan":
            # Dealing with the invesitgate
            k = "Investigate"

            user_message_inv = {
                "role": "user",
                "content": f"Here are the activities {rp}",
            }

            messages_inv = [inv[0], user_message_inv]

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages_inv,
            )

            rp = response["choices"][0]["message"]["content"]

            responses.append(rp)
            counter += 1

            print(f"Done with query {counter}")

    print(responses)
    respars = ResponseParser.ResponseParser(responses)
    final_response = respars.parse()
    return final_response


# with open("./lesson_plan.text", "w") as f:
#     for k, v in final_response.items():
#         print(v)
#         print(f"type v: {type(v)}")
#         exit(0)
#         f.write(
#             f"-----------------------------------------{k}-----------------------------------------"
#         )
#         f.write("\n")
#         f.write(v)
#         f.write("\n")
