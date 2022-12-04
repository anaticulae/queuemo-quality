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


def pusher(cmd, mp, expect: bool = True):
    return utilatest.run_cov(
        cmd,
        process='pusher',
        main=train.pusher.main,
        mp=mp,
        expect=expect,
    )


# TODO: ENABLE LINUX LATER
@utilatest.no_linux
@utilatest.longrun
def test_pusher_cli_done(td, freeport, mp):
    # TODO: AUTOMATE FREE PORT FINDER
    port = freeport
    root = td.tmpdir
    locomotive = train.loco.create(root, port=port, runtime=10)
    locomotive.start(queuemo_start=False)
    train.performance.waitforstartup(port)
    count = len(utila.file_list(td.tmpdir, recursive=True))
    assert count <= 1
    cmd = f'--newest 5 --port {port}'
    pusher(cmd, mp)
    # shutdown resource receiver
    locomotive.close()
    # wait for shutdown
    locomotive.wait()
    # wait for publish # TODO: IMPROVE LATER
    time.sleep(5.0)
    count = len(utila.file_list(td.tmpdir, recursive=True))
    # one pdf-file and jobinfo for every document
    assert count >= 10


def test_pusher_cli_error(mp, capsys):
    pusher('', mp=mp, expect=False)
    assert 'nothing todo' in utilatest.stderr(capsys)
