# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utila
from utilatest import mp  # pylint:disable=W0611
from utilatest import td  # pylint:disable=W0611

import train

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

# ensure that viewo script is installed
assert utila.hasprog('viewo'), 'install viewo'


@pytest.fixture
def freeport():
    for port in utila.ranges(8000, 8200):
        cmd = f'curl {train.DEV_SERVER_URL}:{port}  --connect-timeout 1'
        completed = utila.run(cmd, expect=None)
        if completed.returncode == 7:
            # curl does not reach the port/goal therefore it is free
            return port
    return None
