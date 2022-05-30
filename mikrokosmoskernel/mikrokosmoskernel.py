#!/usr/bin/python
# -*- coding: utf-8 -*-

from ipykernel.kernelbase import Kernel
from pexpect import popen_spawn
import pexpect
import re
import os
from platform import uname

_IS_WSL = 'Microsoft' in uname().release


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
    banner = "Mikrokosmos - A lambda calculus interpreter (kernel v0.1.8)"

    # Initialization, Windows (and Windows Subsystem for Linux) needs PopenSpawn
    if os.name == 'nt' or _IS_WSL:
        mikro = pexpect.popen_spawn.PopenSpawn('mikrokosmos')
    else:
        mikro = pexpect.spawn('mikrokosmos')
        
    mikro.expect('mikro>')
    
    def do_execute(self, code, silent,
                   store_history=True,
                   user_expressions=None,
                   allow_stdin=False):

        # Windows needs a newline
        is_windows = os.name == 'nt' or _IS_WSL
        if is_windows:
            endofline = '\n'
        else:
            endofline = ''
            
        # Interpreter interaction
        # Multiple-line support
        output = ""
        for line in code.split('\n'):
            # Send code to mikrokosmos
            self.mikro.sendline(line + endofline)
            self.mikro.expect('mikro> ')
            
            # Receive and filter code from mikrokosmos
            partialoutput = self.mikro.before
            partialoutput = partialoutput.replace(b'\x1b>',b'') # Filtering codes
            partialoutput = partialoutput.replace(b'\x1b=',b'') # Filtering codes
            partialoutput = partialoutput.decode('utf8', 'replace')

            # Linux creates a spurious newline
            if not is_windows:
                partialoutput = partialoutput[partialoutput.index('\n')+1:]

            output = output + partialoutput

            # Windows needs to expect because of the previous newline
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
