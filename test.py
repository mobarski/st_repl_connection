import streamlit as st
from st_repl_connection import ReplConnection

#model = st.experimental_connection("repl_llama_cpp_hermes", type=ReplConnection)
#resp = model.query("Compare Linux and MacOS.")
#print(resp)

model = st.experimental_connection("repl_python", type=ReplConnection)
resp = model.query("7*6")
print(resp)
