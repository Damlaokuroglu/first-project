# Bu kod Langchain ve Streamlit kullanarak bir blog yazısı için taslak oluşturmamıza yardımcı olacak bir uygulama oluşturur. 

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate    # PromptTemplate bir metin şablonu oluşturur.

st.title("🦜🔗 Langchain - Blog Outline Generator App")

openai_api_key = "sk-proj-CjCrQtfnzXk6DJdWlB6lT3BlbkFJ5g9P1a0uUZQEb284IFnB"

# openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

# blog_outline fonksiyonu blog için topic konusunda bir taslak oluşturur. template değişkeni dil modelinin belirli bir görevi nasıl yerine getireceğini anlatan bir şablon metnini içerir. {topic} şablon metninde yer tutucu (placeholder) olarak kullanılır. Kullanıcının girdiği konu {topic}'e yerleşir. input_variables parametresi şablon metnindeki yer tutucuların hangi giriş değişkenleri ile doldurulacağını belirtir. template=template parametresi tanımlanan şablon metnini belirtir. prompt, PromptTemplate sınıfından oluşturulmuş bir nesnedir. format metodu şablondaki yer tutucuları belirli giriş verileri ile doldurur. llm dil modeline prompt_query metni gönderilir ve modelin bu metne yanıt üretmesi sağlanır. 

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