# OpenAI'ın GPT-3.5-turbo modelini kullanarak sohbet botu oluşturur.

# Streamlit ve Openai kütüphaneleri içe aktarılıyor.

import streamlit as st
from openai import OpenAI

# Openai api key'i girdik.
openai_api_key = "sk-proj-CjCrQtfnzXk6DJdWlB6lT3BlbkFJ5g9P1a0uUZQEb284IFnB"

# Streamlit içinde yan panel oluşturur.

with st.sidebar:
    # openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    # Uygulamanın kaynak kodunu sunar.
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    # Kullanıcıya uygulamayı GitHub Codespaces üzerinde açmak için bağlantıyı verir.
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

# Uygulamanın başlığını belirler.

st.title("💬 Chatbot")

# st.session_state oturum durumunu kontrol edip veri depolanmasını sağlar. st.session_state içinde messages anahtarı yoksa true döner ve assistant rolünde varsayılan bir mesaj ile uygulama başlatılır.

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Bu kod oturum durumundaki tüm mesajları ekranda görüntüler. İlk satır tüm mesajları döngü yapar, ikinci satır tüm mesajları rolüne göre sohbet balonu oluşturarak ekranda mesaj içeriklerini gösterir. st.session_state.messages oturum durumundaki önceki tüm mesajların rolünü ve içeriğini dictionary olarak saklar. st.chat_message(role) streamlit'in sohbet mesajlarını görüntülemek için kullandığı bir fonksiyondur. msg["role"] döngüdeki mevcut mesajın rolünü alır. .write(content) mesaj içeriğini ekranda görüntüler. msg["content"] döngüdeki mevcut mesajın içeriğini alır.

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# prompt kullanıcıdan alınan metni temsil eden bir değişkendir. st.chat_input() kullanıcıdan metin girişi almayı sağlar. Kullanıcının yazdığı değer prompt değişkenine atanır ve eğer bu değişken boş değilse kullanıcı bir şeyler yazdıysa if bloğu çalışır. Walrus operatörü := bir ifadeyi değerlendirirken aynı zamanda bir değişkene atama yapmayı sağlar. prompt değişkeninin sadece if bloğunda kullanılmasını da sağlar. 

if prompt := st.chat_input():

    # if not openai_api_key:
    #     st.info("Please add your OpenAI API key to continue.")
    #     st.stop()

    # Bu kod OpenAI api'sine erişim sağlamak için gerekli istemciyi oluşturur. Bu nesne api ile etkileşime geçmek için kullanılır. OpenAI, openai api'sine erişmek için kullanılan bir kütüphanedir. OpenAI bir sınıfsa bu sınıfın örneğini(client) oluşturur, bir fonksiyonsa bunu kullanarak API'ye erişim sağlar. api_key=openai_api_key kullanılan API anahtarını belirtir. openai_api_key API anahtarının sağlandığı değişkendir. client değişkeni OpenAI api'sine erişmek ve api çağrıları yapmak için kullanılan istemci nesnesini ifade eder. Bu istemci OpenAI api'sine istekler göndermek için kullanılacak. api_key parametresi OpenAI api'sinin kimlik doğrulaması için kullanılır. 

    client = OpenAI(api_key=openai_api_key)

    # İlk satır kullanıcının sohbet penceresine yazdığı mesajı listenin sonuna ekler. .append() metodu listeye yeni bir öğe ekler. ikinci satır kullanıcının girdiği mesajı sohbet penceresinde gösterir.  

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # .chat OpenAI api'sindeki sohbet işlevlerine erişim sağlar. .completions api'nin tamamlama özelliğini temsil eder, genelde modelin bir sohbete yanıt oluşturması için kullanılır. .create yeni bir tamamlanma oluşturur, OpenAI modelinin kullanılarak yanıt üretilmesini sağlar. messages api çağrısına gönderilen mesajlar dizisini belirtir. st.session_state.messages listesi modelin yanıt oluştururken tüm mesaj geçmişini dikkate almasını sağlar. Bu yanıtı response değişkeninde saklar.

    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)

    # OpenAI api'sinden gelen yanıtı sohbet penceresinde gösterip sohbet geçmişine ekler. response.choices[0] birden fazla yanıt seçeneği varsa ilk yanıtı seçer. 

    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)     # Yanıt sadece metin türünde olur. 

# Streamlit'in etkileşimli doğası sayesinde kod tamamen çalıştıktan sonra yeniden çalışıp kullanıcıdan soru alır. 