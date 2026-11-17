# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utilo
from utilotest import mp  # pylint:disable=W0611
from utilotest import td  # pylint:disable=W0611

import train

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

# ensure that viewo script is installed
assert utilo.hasprog('viewo'), 'install viewo'


@pytest.fixture(autouse=True)
def setup_env(monkeypatch, testdir):
    monkeypatch.setenv("VIEWO_HELPDESK", str(testdir.tmpdir))


def find_free_port() -> int:
    assert utilo.hasprog('curl')
    for port in utilo.ranges(8000, 8200):
        cmd = f'curl http://{train.DEV_SERVER_URL}:{port}  --connect-timeout 1'
        completed = utilo.run(cmd, expect=None)
        if completed.returncode == 7:
            # curl does not reach the port/goal therefore it is free
            return int(port)
    return None


@pytest.fixture
def freeport():
    return find_free_port()
