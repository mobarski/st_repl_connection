import streamlit as st
from st_repl_connection import ReplConnection

st.set_page_config(layout="wide", page_title='llama.cpp REPL demo #2')
ss = st.session_state

COLUMNS = 0.2, 1.5, 0.5, 2, 0.5, 2, 0.2

# HEADER
_,c1,_,c2,_,c3,_ = st.columns(COLUMNS)
c1.header('')
with c2:
    st.header('Hermes')
    model1 = st.experimental_connection("repl_llama_cpp_hermes", type=ReplConnection)
with c3:
    st.header('Wizard')
    model2 = st.experimental_connection("repl_llama_cpp_wizard", type=ReplConnection)
st.divider()

# HISTORY
if 'history' not in ss: ss.history=[]
for p,resp1,resp2 in ss.history:
    _,c1,_,c2,_,c3,_ = st.columns(COLUMNS)
    c1.write(f'##### {p}')
    c2.write(resp1)
    c3.write(resp2)
    st.divider()

# PROMPT
prompt = st.chat_input('Prompt for the model or /reset')

# RESPONSE
_,c1,_,c2,_,c3,_ = st.columns(COLUMNS)
if prompt == '/reset':
    ss.history = []
    for col,model in ((c2,model1),(c3,model2)):
        with col:
            with st.spinner('resetting...'):
                model.reset()
    st.experimental_rerun()
elif prompt:
    c1.write(f'##### {prompt}')
    with c2:
        resp1 = model1.query(prompt, ttl=0).strip()
        st.write(resp1)
    with c3:
        resp2 = model2.query(prompt, ttl=0).strip()
        st.write(resp2)
    ss.history.append((prompt,resp1,resp2))
