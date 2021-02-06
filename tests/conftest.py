# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import sys

import utila
import utilatest

import train

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name


def pytest_sessionstart(session):  # pylint:disable=W0613
    if 'PYTEST_XDIST_WORKER' in os.environ:
        # master process only
        return

    single_test = '-k' in sys.argv
    if not single_test and ('GENERATE' in os.environ or utilatest.LONGRUN):
        utila.log('install requirements')
        utilatest.clean_install(train.ROOT, train.PROCESS)
