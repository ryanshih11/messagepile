import os
import threading
import subprocess

class Runner():
    def run_code(self, language, code, args=[]):
        self.code_file = '/tmp/code'

        with open(self.code_file, 'w') as f:
            f.write(code)
        
        result = getattr(self, language)(args)
        os.remove(self.code_file)
        return result

    def generic_interpreter(self, path, args):
        command = [path, self.code_file]
        command.extend(args)
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        return p.communicate()
    
    def python(self, args):
        return self.generic_interpreter('/usr/bin/python', args)
    
    def java_cleanup_thread(self):
        os.system('sleep 5; rm /tmp/Main.java /tmp/Main.class')
        return "Look at you poking around", "Hmmmm"

    def java(self, args):
        os.system('cp /tmp/code /tmp/Main.java; javac /tmp/Main.java')
        env = os.environ.copy()
        env['CLASSPATH'] = '/tmp'
        command = ['/usr/bin/java', 'Main']
        command.extend(args)
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, env=env)
        threading.Thread(target=self.java_cleanup_thread).start()
        return p.communicate()

    def brainfuck(self, args):
        return self.generic_interpreter('/usr/bin/brainfuck', args)
    
    def php(self, args):
        return self.generic_interpreter('/usr/bin/php', args)

    def go_cleanup_thread(self):
        os.system('sleep 5; rm /tmp/code.go /tmp/codego')
        return "Look at you poking around", "Hmmmm"

    def go(self, args):
        os.system('cp /tmp/code /tmp/code.go; export GOPATH=/tmp; cd /tmp; go build -o /tmp/codego')
        command = ['/tmp/codego']
        command.extend(args)
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        #threading.Thread(target=self.go_cleanup_thread).start()
        return p.communicate()
    
    def rust_cleanup_thread(self):
        os.system('sleep 5; rm /tmp/a.out')
        return "Look at you poking around", "Hmmmm"

    def rust(self, args):
        compile_proc = subprocess.Popen(['/usr/bin/rustc', self.code_file, '-o', '/tmp/a.out'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        os.system('sleep 5')
        command = ['/tmp/a.out']
        command.extend(args)
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        threading.Thread(target=self.rust_cleanup_thread).start()
        return p.communicate()