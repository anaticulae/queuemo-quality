# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import utilo
import utilotest

import train.performance

PARAMETER = [
    pytest.param(item, port, id=utilo.file_name(item))
    for port, item in enumerate(hoverpower.PDF, start=3500)
]


@utilotest.monday
@pytest.mark.parametrize('path, port', PARAMETER)
def test_cli_hoverpower(path, port, td):
    train.performance.run(
        td.tmpdir,
        path,
        port,
    )
