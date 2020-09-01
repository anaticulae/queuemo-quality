#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import os
import subprocess
import time

import utila

import train.loco

PORT = 4444
SERVER = 'http://localhost'


def wait(process):
    completed = train.loco.check_process(process)
    while completed is None:
        completed = train.loco.check_process(process)
        time.sleep(1.0)
    return completed


def upload(file: str, server: str = SERVER, port: int = PORT):
    base, filename = os.path.split(file)
    cmd = f'curl -F "file=@{filename}" {server}:{port}/upload'
    completed = utila.run(cmd, cwd=base)
    assert completed.returncode == utila.SUCCESS, str(completed)


def run(workspace, source, port=PORT) -> str:
    cmd = f'train --workspace {workspace} -j=1 -p={port} -r=1000'
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    # ensure correct startup
    time.sleep(10.0)
    returncode = train.loco.check_process(process)
    assert returncode is None, returncode

    # upload test file
    upload(file=source, port=port)

    # wait for finish processing
    returncode = wait(process)
    assert returncode == utila.SUCCESS, returncode

    ready = os.path.join(workspace, 'ready')
    count = utila.file_count(ready)
    assert count >= 15, ready
    return ready
