from st_repl_connection import ReplController

with ReplController('python3 -i', '>>> ') as app:
    print(app.send('6 * 7'))
    print(app.send('128 + 2**7'))
