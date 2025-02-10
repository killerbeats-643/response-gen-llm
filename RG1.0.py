#working good
#version 1
#generating response from the model 
import streamlit as st
import google.generativeai as genai

# Set up the API key
GOOGLE_API_KEY = 'AIzaSyDajKi-J1o1d0Us9dZcHP4JqkSFIgPaY_s'
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-1.5-pro")

# Ensure session state variable for questions exists
if "questions" not in st.session_state:
    st.session_state.questions = []

# Title for the form
st.title("Form Title")
title = st.text_input("", placeholder="Enter your title...")

# Function to add a new question
def add_question():
    st.session_state.questions.append({"type": None, "text": "", "response": ""})

# Function to query the model for suggestions based on the title and questions
def model_suggestion(title,question_type, questions_list):
    prompt = (
        f"Analyze the title: {title} , question type {question_type} and the previous questions: {questions_list}. "
        "Then suggest relevant questions along with the response types. "
        "Response types can include: Text Box, Integer, File Input (doc, image, etc.), "
        "Rating/Scale Questions, Date, Binary (Yes/No), Dropdown (multiple choices). "
        "Please avoid repeating content and strictly provide the response in json format"
    )
    # prompt = (
    # f"Analyze the following input: \n"
    # f"1. Title: {title} \n"
    # f"2. Question Type: {question_type} \n"
    # f"3. Previous Questions: {questions_list} \n\n"
    # "Based on the analysis, suggest a list of relevant new questions with their corresponding response types. "
    # "Ensure that the suggested questions are distinct from the previous ones and are contextually relevant to the provided title and question type. "
    # "The possible response types are: Text Box, Integer, File Input (doc, image, etc.), Rating/Scale Questions, Date, Binary (Yes/No), and Dropdown (multiple choices). "
    # "Please strictly provide the output in JSON format, following this structure: \n\n"
    # "{\n"
    # "{'question': '<Suggested Question>', 'response_type': '<Suggested Response Type>'},\n"
    # "...\n"
    # "]\n"
    # "}")


    print("Title", title)
    print("Question type", question_type)
    print("Questions ", questions_list)

    try:
        response = model.generate_content(prompt)
    
        if response and hasattr(response, 'text'):  # Ensure the response contains text
            return response.text.strip()
        else:
            return "No response from the model."
    except Exception as e:
        return f"Error querying the Gemini model: {e}"

# Button to add questions
if st.button("+ Add Question"):
    add_question()

# Display all questions and allow user interaction
for idx, question in enumerate(st.session_state.questions):
    st.subheader(f"Question {idx + 1}")

    # Select question type
    question_type = st.selectbox(
        f"Select Question Type {idx + 1}",
        ["None","date", "Multiple Choice", "Short Answer", "Yes/No", "Rating Scale"],
        key=f"type_{idx}",
        index=["None","date", "Multiple Choice", "Short Answer", "Yes/No", "Rating Scale"].index(question["type"]) if question["type"] else 0
    )

    # Enter question text
    question_text = st.text_input(
        f"Enter Question {idx + 1}",
        value=question["text"],
        key=f"text_{idx}",
        placeholder="Enter your question..."
    )

    # Determine response type based on question type
    response_type_mapping = {
        "Multiple Choice": "Dropdown / Radio Buttons",
        "Short Answer": "Text Input",
        "Yes/No": "Yes or No",
        "Rating Scale": "Stars / Slider / Number Scale"
    }
    response_type = response_type_mapping.get(question_type, "")

    if response_type:
        st.write(f"Response Type: {response_type}")

    # Update session state with latest values
    st.session_state.questions[idx] = {
        "type": question_type if question_type else None,
        "text": question_text,
        "response": response_type
    }

# If a title is entered and there are questions, allow calling the model for suggestions
if title and len(st.session_state.questions) > 0:
    if st.button("CALL MODEL"):
        suggestions = model_suggestion(title,question_type, st.session_state.questions)
        st.write(suggestions)

