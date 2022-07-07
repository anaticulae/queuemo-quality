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

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

# ensure that viewo script is installed
utila.run('where viewo')


@pytest.fixture
def freeport():
    for port in range(6000, 6100):
        cmd = f'curl http://localhost:{port}  --connect-timeout 1'
        completed = utila.run(cmd, expect=None)
        if completed.returncode == 7:
            # curl does not reach the port/goal therefore it is free
            return port
    return None
