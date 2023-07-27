# Streamlit ReplConnection

Connect to local REPL applications from your [Streamlit](https://streamlit.io/) app.

For example you can control [llama.cpp](https://github.com/ggerganov/llama.cpp) session from your app!

> Why connect in this way and not via wrapper like [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)?
>
> - You don't have to wait for the wrapper update and can use the newest features.
> - You can run in on machines without a c/cpp compiler.
> - It's easier to deploy.
>

![screenshot](static/screenshot1.png)



## Installation

```
pip install git+https://github.com/mobarski/st_repl_connection
```



## Quick demonstration

```python
import streamlit as st
from st_repl_connection import ReplConnection

model = st.experimental_connection("llama_cpp_hermes", type=ReplConnection)
resp = model.query('Compare Linux and MacOS.')
st.write(resp)
```



## Main methods



#### query()

`app.query(text, ttl=None) -> str`

- `text` - text to send to the application
- `ttl` - cache the response for `ttl` seconds, `None` -> no caching



## Connection parameters



- `command` - command to execute to run the REPL application
- `prompt` - prompt used by the REPL application (`'>>> '` for python, `'> '` for llama.cpp, etc)
- `encoding` - text encoding used by the REPL application, default: `'utf8'`



You can read about connections in [this section](https://docs.streamlit.io/library/api-reference/connections/st.experimental_connection) of Streamlit documentation.



## Usage examples



##### simple_app.py

```python
import streamlit as st
from st_repl_connection import ReplConnection

model = st.experimental_connection("llama_cpp_hermes", type=ReplConnection)
resp = model.query('Compare Linux and MacOS.')
st.write(resp)
```



##### chat_app.py

```python
import streamlit as st
ss = st.session_state

from st_repl_connection import ReplConnection
model = st.experimental_connection("llama_cpp_hermes", type=ReplConnection)

if 'history' not in ss:
    ss.history = []
for msg in ss.history:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])
    
prompt = st.chat_input('Your message or /clear')
if prompt == '/clear':
    ss.history = []
    st.experimental_rerun()
elif prompt:
    with st.chat_message('user'):
        st.markdown(prompt)
        ss.history.append({'role': 'user', 'content': prompt})
    resp = model.query(prompt)
    with st.chat_message('assistant'):
        st.markdown(resp)
        ss.history.append({'role': 'assistant', 'content': resp})
```

###### chat questions ideas

```
- What is your name?
- What is your quest?
- What is your favorite color?
- What is the capital of Assyria?
- What is the airspeed velocity of an unladen swallow?
- Compare Linux and MacOS.
- Show example of a markdown table.
- Count frequency of words in a file using python.
- Compare PbtA and FitD.
```



##### Usage without streamlit

```python
from st_repl_connection import ReplController

with ReplController('python3 -i', '>>> ') as app:
    print(app.send('6 * 7'))
    print(app.send('128 + 2**7'))
```



## Configuration examples

The configuration is stored in Streamlit's [secrets.toml](https://docs.streamlit.io/library/advanced-features/secrets-management) file (~/.streamlit/secrets.toml on Linux).

You can find more information about managing connections in [this section](docs.streamlit.io/library/advanced-features/connecting-to-data#global-secrets-managing-multiple-apps-and-multiple-data-stores) of Streamlit documentation.



##### llama.cpp running the Hermes model on a GPU

```
[connections.llama_cpp_hermes]
command = "/opt/llama.cpp/main -m /opt/models/ggml-Hermes-2-step2559-q4_K_M.bin -ins -ngl 100"
prompt = "> "
```



##### python running the turtle module

```
[connections.repl_turtle]
command = "python3 -i -c 'from turtle import *; home()'"
prompt = ">>> "
```



##### sqlite

```
[connections.repl_sqlite]
command = "sqlite3 -box -header"
prompt = "sqlite> "
```

