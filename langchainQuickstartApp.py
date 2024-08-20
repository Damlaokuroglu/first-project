# OpenAI'ın dil modelini kullanarak web uygulaması oluşturur ve kullanıcıların sorularına yanıt verir.

import streamlit as st      # Web uygulaması oluşturmak için kullanılır.
from langchain_openai.llms import OpenAI     # OpenAI sınıfı Langchain kütüphanesinin bir parçasıdır ve OpenAI api ile etkileşim kurmamızı sağlar.

st.title("🦜🔗 Langchain Quickstart App")

openai_api_key = "sk-proj-CjCrQtfnzXk6DJdWlB6lT3BlbkFJ5g9P1a0uUZQEb284IFnB"

with st.sidebar:
    # openai_api_key = st.text_input("OpenAI API Key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

# generate_response fonksiyonu OpenAI dil modelini kullanarak verilen metne yanıt üretir. OpenAI sınıfından bir örnek oluşturduk. temperature modelin yanıtlarının rastgeleliğini belirler. 0.7 değeri modelin yaratıcı ama dengeli yanıt üretmesini sağlar. llm(input_text) input_text parametresini OpenAI dil modeline gönderir. Bu model verilen metne uygun yanıt üretir. st.info() Streamlit'in bilgi mesajı fonksiyonudur. Modelin ürettiği yanıtı uygulamanın arayüzünde bilgi mesajı olarak gösterir. Genelde mavi arka planda vurgulanır. 
# Kullanıcıya sadece bilgi veya sonuç gösteren fonksiyonlarda return kullanılmaz, amaç kullanıcıya bir şeyler göstermektir ve doğrudan kullanıcı arayüzüne etki eder. Yanıtı başka fonksiyon veya işlemle kullanmak isteseydik(değer döndürmek) return kullanırdık.

def generate_response(input_text):
    llm = OpenAI(temperature=0.0, openai_api_key=openai_api_key)
    response = llm.invoke(input_text)
    st.info(response)
    # st.info(llm(input_text))

# Bu kod Streamlit'te bir form oluşturur. with bloğu kullanılarak formun içeriği tanımlanır. st.text_area kullanıcının metin girmesini sağlayan alan oluşturur. Enter text metin alanının üstünde bulunan etikettir, başlıktır. Metin alanında varsayılan olarak doldurulan başlangıç metni vardır. st.form_submit_button("Submit") formun gönderilmesi için bir buton oluşturur. Bu buton tıklandığında form gönderilir ve formdaki veriler işlenir. submitted değişkeni formun gönderilip gönderilmediğini kontrol eder. Buton tıklandıysa True olur. Eğer api anahtarı mevcutsa ve submitted = True ise generate_response fonksiyonu çağırılır ve text değişkenindeki metni bu fonksiyona geçirir. Bu fonksiyon OpenAI api'sine metni gönderir ve yanıtı alır.

with st.form("my_form"):
    text = st.text_area("Enter text:", "What are 3 key advice for learning how to code?")
    submitted = st.form_submit_button("Submit")
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    elif submitted:
        generate_response(text)