# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import train.loco
import train.performance


@pytest.mark.timeout(60)
def test_locomotive_run(td, freeport):
    root = td.tmpdir
    locomotive = train.loco.create(
        root,
        port=freeport,
    )
    locomotive.start()
    result = locomotive.wait()
    assert not result.queuemo, str(result)
