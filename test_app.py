import streamlit as st
ss = st.session_state

from st_repl_connection import ReplConnection
model = st.experimental_connection("repl_llama_cpp_hermes", type=ReplConnection)

if 'history' not in ss:
    ss.history = []
for msg in ss.history:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])
    
prompt = st.chat_input('Your message or /clear')
if prompt == '/clear':
    model.reset()
    ss.history = []
    st.experimental_rerun()
elif prompt:
    with st.chat_message('user'):
        st.markdown(prompt)
        ss.history.append({'role': 'user', 'content': prompt})
    resp = model.query(prompt, ttl=0)
    with st.chat_message('assistant'):
        st.markdown(resp)
        ss.history.append({'role': 'assistant', 'content': resp})

