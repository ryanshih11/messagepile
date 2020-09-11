import os
import threading
import subprocess

class Runner():
    def run_code(self, language, code):
        self.code_file = '/tmp/code'

        with open(self.code_file, 'w') as f:
            f.write(code)
        
        result = getattr(self, language)()
        os.remove(self.code_file)
        return result

    def generic_interpreter(self, path):
        p = subprocess.Popen([path, self.code_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        return p.communicate()
    
    def python(self):
        return self.generic_interpreter('/usr/bin/python')
    
    def java_cleanup_thread(self):
        os.system('sleep 5; rm /tmp/Main.java /tmp/Main.class')
        return "Look at you poking around", "Hmmmm"

    def java(self):
        os.system('cp /tmp/code /tmp/Main.java; javac /tmp/Main.java')
        env = os.environ.copy()
        env['CLASSPATH'] = '/tmp'
        p = subprocess.Popen(['/usr/bin/java', 'Main'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, env=env)
        threading.Thread(target=self.java_cleanup_thread).start()
        return p.communicate()

    def brainfuck(self):
        return self.generic_interpreter('/usr/bin/brainfuck')
    
    def php(self):
        return self.generic_interpreter('/usr/bin/php')

    def go_cleanup_thread(self):
        os.system('sleep 5; rm -rf /tmp/src')
        return "Look at you poking around", "Hmmmm"

    def go(self):
        os.system('mkdir /tmp/src; mkdir /tmp/src/code; cp /tmp/code /tmp/src/code/code.go')
        env = os.environ.copy()
        env['GOPATH'] = '/tmp'
        p = subprocess.Popen(['/usr/bin/go', 'run', 'code'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, env=env)
        threading.Thread(target=self.go_cleanup_thread).start()
        return p.communicate()
    
    def rust_cleanup_thread(self):
        os.system('sleep 5; rm /tmp/a.out')
        return "Look at you poking around", "Hmmmm"

    def rust(self):
        compile_proc = subprocess.Popen(['/usr/bin/rustc', self.code_file, '-o', '/tmp/a.out'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        os.system('sleep 5')
        p = subprocess.Popen(['/tmp/a.out'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        threading.Thread(target=self.rust_cleanup_thread).start()
        return p.communicate()