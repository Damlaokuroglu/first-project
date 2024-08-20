# Streamlit ile basit bir web uygulaması oluşturur ve Langchain kütüphanesini kullanarak web araması yapan sohbet botu oluşturur.

import streamlit as st

from langchain.agents import initialize_agent, AgentType # Belirli görevleri yerine getirebilecek ajanlar oluşturmayı sağlar. Ajanın belirli açıklamaya göre hareket etmesini sağlar.
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler # Üretilen çıktıların uygulamada gösterilmesini(geri çağırma işleyicisi) sağlar. Ajanın yanıtlarını kullanıcı arayüzünde dinamik olarak güncelleyebilir.
from langchain_community.chat_models import ChatOpenAI # OpenAI api'sini kullanarak dil modelini sohbet botu olarak yapılandırabilir.
from langchain_community.tools import DuckDuckGoSearchRun # DuckDuckGo arama motorunu kullanarak web'de arama yapabilir. 

with st.sidebar:
    # openai_api_key = st.text_input("OpenAI API Key", key="langchain_search_api_key_openai", type="password")
    openai_api_key = "sk-proj-CjCrQtfnzXk6DJdWlB6lT3BlbkFJ5g9P1a0uUZQEb284IFnB"
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/2_Chat_with_search.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("🔎 LangChain - Chat with search")

"""
In this example, we're using `StreamlitCallbackHandler` to display the thoughts and actions of an agent in an interactive Streamlit app.
Try more LangChain 🤝 Streamlit Agent examples at [github.com/langchain-ai/streamlit-agent](https://github.com/langchain-ai/streamlit-agent).
"""     # Çok satırlı dizeleri belirtmek için 3 tırnak kullanılır.

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Kullanıcıya yer tutucu ile bir soru sorulur. Bu, kullanıcının ne tür bir bilgi girmesi gerektiğini belirtir. 

if prompt := st.chat_input(placeholder="Who won the Women's U.S. Open in 2018?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # if not openai_api_key:
    #     st.info("Please add your OpenAI API key to continue.")
    #     st.stop()

    # llm değişkeni ChatOpenAI sınıfı tarafından oluşturulan dil modeli nesnesini temsil eder. ChatOpenAI OpenAI'ın GPT dil modellerini kullanarak uygulamalar oluşturması için kullanılır. streaming=True yanıtın parça parça akış modunda gelmesini sağlar. 

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, streaming=True)

    # DuckDuckGoSearchRun sınıfı DuckDuckGo arama motorunu kullanarak web aramaları yapmak için kullanılır. name arama aracına verilen isimdir. Aracı tanımlamak ve diğer araçlardan ayırt etmek için kullanılır. 

    search = DuckDuckGoSearchRun(name="Search")

    # initialize_agent verilen araçlar ve dil modeli ile belirli görevleri yerine getirmek için bir ajan oluşturur ve yapılandırır. AgentType.ZERO_SHOT_REACT_DESCRIPTION ajanı örnekler olmadan görevini yerine getirebilir. React Description ajanın görevleri nasıl yerine getireceğine dair açıklamaları kullanarak hareket edeceğini belirtir. handle_parsing_errors=True ajanın analiz sırasında karşılaşacağı hataları yönetmesine olanak tanır.  

    search_agent = initialize_agent([search], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True)

    # st.chat_message("assistant") Streamlit'te bir sohbet mesajı bloğu oluşturur. st.container() Streamlit'te bir kapsayıcı oluşturur. Geri çağırma işleyicisinin(callbackhandler) çıktısını görüntülemek için kullanılır. expand_new_thoughts=False yeni düşünceleri genişletme özelliğini devre dışı bırakır. search_agent.run daha önce oluşturulan arama ajanını çalıştırır. callbacks=[st_cb] ajan çalışırken geri çağırma işleyicisinin eylemleri görüntülemesini sağlar. response kulllanıcının sorgusuna verilen yanıttır. 

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = search_agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)

# StreamlitCallbackHandler sayesinde (expand_new_thoughts parametresi) bot yanıt üretirken Thinking... yazar. 