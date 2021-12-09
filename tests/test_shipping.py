# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hardcore
import power
import pytest
import utilatest

import train.loco
import train.performance


def test_locomotive_run(testdir):
    root = testdir.tmpdir
    locomotive = train.loco.create(root, port=train.performance.PORT)
    locomotive.start()
    result = locomotive.wait()
    assert not result.queuemo, str(result)


@pytest.mark.parametrize('public', [True, False])
@utilatest.nightly
def test_publish(public, testdir):
    port = 4444 if public else 4445
    root = testdir.tmpdir
    locomotive = train.loco.create(root, port=port, runtime=10)
    locomotive.start()

    train.performance.upload(file=power.HOME018_PDF, public=public, port=port)

    result = locomotive.wait(None)
    assert not result.queuemo, str(result)


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
    train.performance.run(workspace, file, port)


ALL = hardcore.F0 + hardcore.F50 + hardcore.F100 + hardcore.F200 + hardcore.F300
HARDCORE = [
    pytest.param(
        item,
        port,
        id=utilatest.simplify_testfile_names((hardcore.ROOT, item))[0],
    ) for port, item in enumerate(ALL, start=4000)
]


@utilatest.skip_nightly
@pytest.mark.parametrize('file, port', HARDCORE)
def test_hardcore(file, port, testdir):
    workspace = str(testdir.tmpdir)
    train.performance.run(workspace, file, port)
