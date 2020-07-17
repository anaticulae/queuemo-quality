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

import power
import pytest
import utila
import utilatest

import train.loco

PORT = 4444
SERVER = 'http://localhost'


def test_locomotive_run(testdir):
    root = testdir.tmpdir
    locomotive = train.loco.create(root, viewo=4444)
    locomotive.start()

    result = locomotive.wait()
    assert result.queuemo == 0, str(result)


@utilatest.skip_longrun
def test_publish(testdir):
    port = 4444
    root = testdir.tmpdir
    locomotive = train.loco.create(root, viewo=port, runtime=10)
    locomotive.start()

    upload(file=power.MASTER072_PDF)

    result = locomotive.wait(None)
    assert result.queuemo == 0, str(result)


def upload(file: str, server: str = SERVER, port: int = PORT):
    base, filename = os.path.split(file)
    cmd = f'curl -F file=@{filename} {server}:{port}/upload'
    completed = utila.run(cmd, cwd=base)
    assert completed.returncode == utila.SUCCESS, str(completed)


PARAMETER = [
    pytest.param(
        item,
        port,
        id=utilatest.simplify_testfile_names((power.REPOSITORY, item))[0],
    ) for port, item in enumerate(power.PDF, start=3500)
]


@utilatest.skip_nightly
@pytest.mark.parametrize('file, port', PARAMETER)
def test_cli(file, port, testdir):
    workspace = str(testdir.tmpdir)

    cmd = f'train --workspace {workspace} -j=1 -p={port} -r=1000'
    process = subprocess.Popen(cmd)

    # ensure correct startup
    time.sleep(10.0)
    returncode = train.loco.check_process(process)
    assert returncode is None, returncode

    # upload test file
    upload(file=file, port=port)

    # wait for finish processing
    returncode = wait(process)
    assert returncode == utila.SUCCESS, returncode

    ready = os.path.join(workspace, 'ready')
    count = utila.file_count(ready)
    assert count >= 15, ready


def wait(process):
    completed = train.loco.check_process(process)
    while completed is None:
        completed = train.loco.check_process(process)
        time.sleep(1.0)
    return completed
