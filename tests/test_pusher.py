# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import time

import utila
import utilatest

import train.loco
import train.performance
import train.pusher


def pusher(cmd, monkeypatch, success: bool = True):
    return utilatest.run_command(
        cmd,
        process='pusher',
        main=train.pusher.main,
        monkeypatch=monkeypatch,
        success=success,
    )


def test_pusher_cli_done(testdir, freeport, monkeypatch):
    # TODO: AUTOMATE FREE PORT FINDER
    port = freeport
    root = testdir.tmpdir
    locomotive = train.loco.create(root, port=port, runtime=10)
    locomotive.start(queuemo_start=False)
    train.performance.waitforstartup(port)
    count = len(utila.file_list(testdir.tmpdir, recursive=True))
    assert count <= 1
    cmd = f'--newest 5 --port {port}'
    pusher(cmd, monkeypatch)
    # shutdown resource receiver
    locomotive.close()
    # wait for shutdown
    locomotive.wait()
    # wait for publish # TODO: IMPROVE LATER
    time.sleep(5.0)
    count = len(utila.file_list(testdir.tmpdir, recursive=True))
    # one pdf-file and jobinfo for every document
    assert count >= 10


def test_pusher_cli_error(monkeypatch, capsys):
    pusher('', monkeypatch=monkeypatch, success=False)
    assert 'nothing todo' in utilatest.stderr(capsys)
