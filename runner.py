import os
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