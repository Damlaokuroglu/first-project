import streamlit as st 
from langchain_openai.llms import OpenAI 

st.title("🦜🔗 Langchain Quickstart App")

openai_api_key = "sk-proj-CjCrQtfnzXk6DJdWlB6lT3BlbkFJ5g9P1a0uUZQEb284IFnB"

with st.sidebar:
    # openai_api_key = st.text_input("OpenAI API Key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

def generate_response(input_text):
    llm = OpenAI(temperature=0.0, openai_api_key=openai_api_key)
    response = llm.invoke(input_text)
    st.info(response)
    # st.info(llm(input_text))

with st.form("my_form"):
    text = st.text_area("Enter text:", "What are 3 key advice for learning how to code?")
    submitted = st.form_submit_button("Submit")
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    elif submitted:
        generate_response(text)
