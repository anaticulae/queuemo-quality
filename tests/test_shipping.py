# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import subprocess
import time

import utila

import tests.resources
import train.loco

PORT = 4444
SERVER = 'http://localhost'


def test_locomotive_run(testdir):
    root = testdir.tmpdir
    locomotive = train.loco.create(root, viewo=4444)
    locomotive.start()

    result = locomotive.wait()

    assert result.queuemo == 0, str(result)


@utila.skip_longrun
def test_publish(testdir):
    port = 4444
    root = testdir.tmpdir
    locomotive = train.loco.create(root, viewo=port, runtime=10)
    locomotive.start()

    upload(file=tests.resources.MASTER72)

    result = locomotive.wait(None)
    assert result.queuemo == 0, str(result)


def upload(file: str, server: str = SERVER, port: int = PORT):
    base, filename = os.path.split(file)
    cmd = f'curl -F file=@{filename} {server}:{port}/upload'
    completed = utila.run(cmd, cwd=base)
    assert completed.returncode == utila.SUCCESS, str(completed)


@utila.skip_longrun
def test_cli(testdir):
    port = 3500
    source = tests.resources.MASTER72
    workspace = str(testdir.tmpdir)

    cmd = f'train --workspace {workspace} -j=1 -p={port} -r=1000'
    process = subprocess.Popen(cmd)

    # ensure correct startup
    time.sleep(10.0)
    returncode = train.loco.check_process(process)
    assert returncode is None, returncode

    # upload test file
    upload(file=source, port=port)

    # wait for finish processing
    returncode = wait(process)
    assert returncode == utila.SUCCESS, returncode


def wait(process):
    completed = train.loco.check_process(process)
    while completed is None:
        completed = train.loco.check_process(process)
        time.sleep(1.0)
    return completed
