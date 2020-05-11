# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import train.loco


def test_shipping(testdir):
    root = testdir.tmpdir
    locomotive = train.loco.create(root, viewo=4444)
    locomotive.start()

    result = locomotive.run()

    assert result.queuemo == 0, str(result)
