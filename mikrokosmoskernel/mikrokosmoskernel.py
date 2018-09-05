#!/usr/bin/python
# -*- coding: utf-8 -*-

from ipykernel.kernelbase import Kernel
from pexpect import popen_spawn
import pexpect
import re
import os

class MikrokosmosKernel(Kernel):
    implementation = 'IMikrokosmos'
    implementation_version = '0.8'
    language = 'mikrokosmos'
    language_version = '0.8'
    language_info = {
        'name' : 'Mikrokosmos',
        'mimetype': 'text/plain',
        'file_extension': '.mkr',
        'codemirror_mode': 'mikrokosmos'
    }
    banner = "Mikrokosmos - A lambda calculus interpreter"

    # Initialization, Windows needs PopenSpawn.
    is_windows = (os.name == 'nt')

    if is_windows:
        mikro = pexpect.popen_spawn.PopenSpawn('mikrokosmos')
        endofline = '\n'
    else:
        mikro = pexpect.spawn('mikrokosmos')
        endofline = ''
        
    mikro.expect('mikro>')
    
    def do_execute(self, code, silent,
                   store_history=True,
                   user_expressions=None,
                   allow_stdin=False):
        
        # Interpreter interaction
        # Multiple-line support
        output = ""
        for line in code.split('\n'):
            # Send code to mikrokosmos
            self.mikro.sendline(line + endofline)
            self.mikro.expect('mikro> ')
            # Receive and filter code from mikrokosmos
            partialoutput = self.mikro.before
            partialoutput = partialoutput.replace('\x1b>','') # Filtering codes
            partialoutput = partialoutput.replace('\x1b=','') # Filtering codes
            partialoutput = partialoutput.decode('utf8')

            if not is_windows:
                partialoutput = partialoutput[partialoutput.index('\n')+1:]

            output = output + partialoutput

            if is_windows:
                self.mikro.expect('mikro> ')
        
        if not silent:
            stream_content = {'name': 'stdout', 'text': output}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }
