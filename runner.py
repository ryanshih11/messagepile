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

    def python(self):
        p = subprocess.Popen(['/usr/bin/python', self.code_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        return p.communicate()
    
    def java_cleanup_thread(self):
        os.system('sleep 5; rm /tmp/Main.java /tmp/Main.class')

    def java(self):
        os.system('cp /tmp/code /tmp/Main.java; javac /tmp/Main.java')
        env = os.environ.copy()
        env['CLASSPATH'] = '/tmp'
        p = subprocess.Popen(['/usr/bin/java', 'Main'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, env=env)
        threading.Thread(target=self.java_cleanup_thread).start()
        return p.communicate()
        