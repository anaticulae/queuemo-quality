# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utilatest

import train.performance

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
