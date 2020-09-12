import os
import inspect
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

    def generic_execute(self, command, args, env=os.environ.copy()):
        calframe_cleanup_func = getattr(self, inspect.getouterframes(inspect.currentframe(), 2)[1][3] + '_cleanup_thread')
        command.extend(args)
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, env=env)
        if calframe_cleanup_func is not None:
            threading.Thread(target=calframe_cleanup_func).start()
        return p.communicate()
        
    def generic_interpreter(self, path, args):
        command = [path, self.code_file]
        return self.generic_execute(command, args)
    
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
        return self.generic_execute(command, args, env)

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
        return self.generic_execute(command, args)

    def rust_cleanup_thread(self):
        os.system('sleep 5; rm /tmp/a.out')
        return "Look at you poking around", "Hmmmm"

    def rust(self, args):
        compile_proc = subprocess.Popen(['/usr/bin/rustc', self.code_file, '-o', '/tmp/a.out'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        os.system('sleep 5')
        command = ['/tmp/a.out']
        return self.generic_execute(command, args)

    def csharp_cleanup_thread(self):
        os.system('rm /tmp/code.exe')
        return "Look at you poking around", "Hmmmm"

    def csharp(self, args):
        os.system('mcs /tmp/code')
        command = ['/usr/bin/mono', '/tmp/code.exe']
        return self.generic_execute(command, args)