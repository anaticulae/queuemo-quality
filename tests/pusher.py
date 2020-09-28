# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import sys

import power

TODO = [
    power.BACHELOR051_PDF,
    power.BACHELOR128_PDF,
    power.BACHELOR200_PDF,
    power.BACHELOR241_PDF,
    power.MASTER031_PDF,
    power.MASTER075_PDF,
    power.MASTER110_PDF,
    power.MASTER112_PDF,
    power.MASTER148_PDF,
    power.MASTER155_PDF,
]

if __name__ == "__main__":
    # fix path setup to avoid importing tests package of other projects
    sys.path.insert(0, os.path.abspath('.'))
    import tests  # isort:skip pylint:disable=wrong-import-position

    for path in TODO:
        tests.upload(path, port=5000)
