# pip install pexpect

from pexpect.popen_spawn import PopenSpawn
import io
from signal import SIGTERM

class ReplController:
    "REPL controller"

    def __init__(self, command, prompt, encoding=None):
        self.command = command
        self.prompt = prompt
        self.encoding = encoding or 'utf8'
        self.proc = None
        self._start()
    
    def send(self, text):
        self.proc.logfile_read = f = io.StringIO()
        self.proc.sendline(text.rstrip())
        self.proc.expect(self.prompt)
        f.seek(0)
        out = f.read()[:-len(self.prompt)]
        return out

    def reset(self):
        self._stop()
        self._start()

    def _start(self):
        self.proc = PopenSpawn(self.command, encoding=self.encoding)
        self.proc.logfile_read = f = io.StringIO()
        self.proc.expect(self.prompt)
        f.seek(0)
        self._start_log = f.read()[:-len(self.prompt)]

    def _stop(self):
        self.proc.logfile_read = f = io.StringIO()
        self.proc.kill(SIGTERM)
        self.proc.wait()
        f.seek(0)
        out = f.read()

    def __enter__(self):
        return self

    def __exit__(self, *args):        
        self.stop()


if __name__=="__main__":
    with ReplController('python3 -i', '>>> ') as p:
        print(f"-->{p.send('7*6')}<--")
        print(f"-->{p.send('2**8')}<--")
        x = p.send(r'print("A\nB\nC")')
        print(f"-->{x}<--")

    with ReplController('/home/mobarski/repo-other/llama.cpp/main -m /home/mobarski/ggml-Hermes-2-step2559-q4_K_M.bin -ins -ngl 100', '> ') as p:
        print(p.send('Compare FitD and PbtA.'))
        print(p.send('Compare Linux and MacOS.'))
        print(p.send('Tell a joke.'))
