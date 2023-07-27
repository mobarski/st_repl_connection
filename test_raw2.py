
from st_repl_connection import ReplController

with ReplController('lama.cpp/main -m ggml-model.bin -ins -ngl 100', '> ') as app:
    print(app.send('What is the capital of Assyria?'))
    print(app.send('What is the airspeed velocity of an unladen swallow?'))
