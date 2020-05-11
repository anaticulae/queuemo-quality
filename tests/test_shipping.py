# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila

import tests.resources
import train.loco

PORT = 4444
SERVER = 'http://localhost'


def test_run_locomotive(testdir):
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
