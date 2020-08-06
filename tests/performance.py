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

import configo
import power
import protocol
import utila

TODO = [
    power.MASTER098_PDF,
    power.MASTER116_PDF,
    power.BACHELOR090_PDF,
    power.HOMEWORK025_PDF,
]


def run():
    # fix path setup to avoid importing tests package of other projects
    sys.path.insert(0, os.path.abspath('.'))
    import tests  # isort:skip pylint:disable=wrong-import-position

    for port, path in enumerate(TODO, start=4700):
        workspace = utila.tmpdir(configo.tmp())
        utila.log(f'run performace for {path} in {workspace} on: {port}')
        ready = tests.run(workspace, path, port=port)
        # load findings by page
        findings = protocol.findings_from_path(ready)
        # global finding list
        findings = utila.flatten([item.content for item in findings])
        # TODO: REPLACE AFTER UPGRADING?
        findings = utila.make_unique(findings)
        utila.log(f'findings: {len(findings)}')


if __name__ == "__main__":
    run()
