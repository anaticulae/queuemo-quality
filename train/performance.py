# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import subprocess
import sys
import time

import utila

import train
import train.loco


def wait(process):
    completed = train.loco.check_process(process)
    while completed is None:  # pylint:disable=W0149
        completed = train.loco.check_process(process)
        time.sleep(1.0)
    return completed


def upload(
    file: str,
    server: str = train.DEV_SERVER_URL,
    port: int = train.DEV_SERVER_PORT,
    public: bool = False,
    verbose: bool = False,
):
    """\
    Args:
        file(str): file upload source
        server(str): ip adress
        port(int): server port
        public(bool): make document accessible by public user
        verbose(bool): if True log curl invocation
    """
    base, filename = os.path.split(file)
    public = '?public=True' if public else ''
    api = f'http://{server}:{port}/api/v0/documents{public}'
    cmd = f'curl -F "file=@{filename}" {api}'
    if verbose:
        utila.log(cmd)
    completed = utila.run(cmd, cwd=base, expect=None)
    if completed.returncode:
        utila.error(cmd)
        utila.error(completed.stderr)
        utila.error('check connection')
        sys.exit(utila.FAILURE)


TWO_HOURS = 3600 * 2


def run(
    workspace,
    source,
    port=train.DEV_SERVER_PORT,
    runtime=TWO_HOURS,
) -> str:
    if not utila.hasprog('train'):
        utila.error('install `train` please')
        sys.exit(127)
    cmd = f'train --workspace {workspace} -j=1 -p={port} -r={runtime}'.split()
    utila.log(cmd)
    with subprocess.Popen(  # nosec
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
    ) as process:
        waitforstartup(port)
        returncode = train.loco.check_process(process)
        assert returncode is None, returncode
        # upload test file
        upload(file=source, port=port, public=True)
        # wait for finished process
        returncode = wait(process)
        assert returncode == utila.SUCCESS, returncode
    ready = os.path.join(workspace, 'ready')
    count = utila.file_count(ready)
    assert count >= 15, ready
    return ready


def waitforstartup(port: int, server: str = train.DEV_SERVER_URL):
    cmd = f'curl http://{server}:{port}'
    # ensure correct startup
    for _ in range(100):
        # curl till server is online
        completed = utila.run(cmd, expect=None)
        if completed.returncode == utila.SUCCESS:
            break
    else:
        utila.error(f'timeout: {cmd}')
        sys.exit(utila.FAILURE)
