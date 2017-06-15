#!/usr/bin/python
# -*- coding: utf-8 -*-

from ipykernel.kernelbase import Kernel
import pexpect

class MikrokosmosKernel(Kernel):
    implementation = 'IMikrokosmos'
    implementation_version = '0.1'
    language = 'mikrokosmos'
    language_version = '0.2'
    language_info = {
        'name' : 'Mikrokosmos',
        'mimetype': 'text/plain',
        'file_extension': '.mkr',
    }
    banner = "Mikrokosmos - A lambda calculus interpreter"

    # Initialization
    mikro = pexpect.spawn('mikrokosmos')
    mikro.expect('mikro>')
    
    def do_execute(self, code, silent,
                   store_history=True,    # Whether to record code in history
                   user_expressions=None,
                   allow_stdin=False):
        
        # Multiple-line support
        output = ""
        for line in code.split('\n'):
            # Send code to mikrokosmos
            self.mikro.sendline(line)
            self.mikro.expect('mikro> ')
            # Receive code from mikrokosmos
            partialoutput = self.mikro.before.decode('utf8')
            output = output + '\n' + partialoutput
        
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
