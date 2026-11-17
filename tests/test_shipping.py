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

import train.loco
import train.performance


@pytest.mark.parametrize('public', [True, False])
def test_publish(public, td):
    port = 4444 if public else 4445
    root = td.tmpdir
    locomotive = train.loco.create(root, port=port, runtime=10)
    locomotive.start()
    # upload a single file
    train.performance.upload(
        file=hoverpower.HOME018_PDF,
        public=public,
        port=port,
    )
    # wait for publishing
    result = locomotive.wait()
    assert not result.queuemo, str(result)
