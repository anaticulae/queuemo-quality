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

import tests.conftest
import train.loco
import train.performance


@utilotest.longrun
@pytest.mark.parametrize('public', [
    pytest.param(True, id='public'),
    pytest.param(False, id='private'),
])
def test_publish(public, td):
    freeport = tests.conftest.find_free_port()
    locomotive = train.loco.create(
        root=td.tmpdir,
        port=freeport,
        runtime=5,
    )
    locomotive.start()
    try:
        # upload a single file
        file = hoverpower.HOME018_PDF
        assert utilo.exists_assert(file)
        train.performance.upload(
            file=file,
            public=public,
            port=freeport,
        )
        # wait for publishing
        result = locomotive.wait(seconds=5)
        assert not result.queuemo, str(result)
    except Exception as testfailure:
        locomotive.close()
        raise testfailure
    locomotive.close()
