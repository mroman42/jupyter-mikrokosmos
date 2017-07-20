#!/usr/bin/python
# -*- coding: utf-8 -*-

from ipykernel.kernelbase import Kernel
import pexpect
import re

class MikrokosmosKernel(Kernel):
    implementation = 'IMikrokosmos'
    implementation_version = '0.1'
    language = 'mikrokosmos'
    language_version = '0.2'
    language_info = {
        'name' : 'Mikrokosmos',
        'mimetype': 'text/plain',
        'file_extension': '.mkr',
        'codemirror_mode': 'mikrokosmos'
    }
    banner = "Mikrokosmos - A lambda calculus interpreter"

    # Initialization
    mikro = pexpect.spawn('mikrokosmos')
    mikro.expect('mikro>')
    
    def do_execute(self, code, silent,
                   store_history=True,
                   user_expressions=None,
                   allow_stdin=False):

        # Lines starting with an space are joined to previous lines
        code = re.sub('\n(\s+)', ' ', code)
        
        # Interpreter interaction
        # Multiple-line support
        output = ""
        for line in code.split('\n'):
            # Send code to mikrokosmos
            self.mikro.sendline(line)
            self.mikro.expect('mikro> ')
            # Receive and filter code from mikrokosmos
            partialoutput = self.mikro.before
            partialoutput = partialoutput.replace(b'\x1b>',b'') # Filtering codes
            partialoutput = partialoutput.replace(b'\x1b=',b'') # Filtering codes
            partialoutput = partialoutput.decode('utf8')
            partialoutput = partialoutput[partialoutput.index('\n')+1:]

            output = output + partialoutput
        
        
        if not silent:
            stream_content = {'name': 'stdout', 'text': output}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }
 
if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=MikrokosmosKernel)
