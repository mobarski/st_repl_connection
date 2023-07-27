from st_repl_connection import ReplController

with ReplController('python3 -i', '>>> ') as py:
    print(py.send('6 * 7'))
    print(py.send('128 + 2**7'))

