# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hardcore
import pytest
import utilatest

import train.performance

ALL = hardcore.F0 + hardcore.F50 + hardcore.F100 + hardcore.F200 + hardcore.F300
HARDCORE = [
    pytest.param(
        item,
        port,
        id=utilatest.simplify_testfile_names((hardcore.ROOT, item))[0],
    ) for port, item in enumerate(ALL, start=4000)
]


@utilatest.nightly
@pytest.mark.parametrize('filepath, port', HARDCORE)
def test_hardcore(filepath, port, testdir):
    train.performance.run(testdir.tmpdir, filepath, port)
