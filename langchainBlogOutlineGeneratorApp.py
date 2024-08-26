import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate 

st.title("🦜🔗 Langchain - Blog Outline Generator App")

openai_api_key = "your_api_key"

def blog_outline(topic):
    # LLM modelinin başlatılması
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)
    # Prompt
    template = "As an experienced data scientist and technical writer, generate an outline for a blog about {topic}."
    prompt = PromptTemplate(input_variables=["topic"], template=template)
    # Prompt şablonunun doldurulması
    prompt_query = prompt.format(topic=topic)
    # LLM modelinin çalıştırılması
    response = llm.invoke(prompt_query)
    # Print results
    return st.info(response)

# st.text_input kullanırsak prompt'un sağ altında press enter to submit form yazar. st.text_area kullanırsak press ctrl+enter to submit form yazar.

with st.form("myform"):
    topic_text = st.text_input("Enter prompt:", "")
    submitted = st.form_submit_button("Submit")
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    elif submitted:
        blog_outline(topic_text)
