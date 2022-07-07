# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utila
import utilatest

import train.performance

PARAMETER = [
    pytest.param(item, port, id=utila.file_name(item))
    for port, item in enumerate(power.PDF, start=3500)
]


@utilatest.nightly
@pytest.mark.parametrize('path, port', PARAMETER)
def test_cli_power(path, port, testdir):
    train.performance.run(
        testdir.tmpdir,
        path,
        port,
    )
