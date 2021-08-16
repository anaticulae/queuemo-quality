# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import sys

import power
import utila

import train
import train.performance

TODO = [
    power.BACHELOR051_PDF,
    power.BACHELOR109_PDF,
    power.BACHELOR128_PDF,
    power.BACHELOR241_PDF,
    power.MASTER031_PDF,
    power.MASTER075_PDF,
    power.MASTER110_PDF,
    power.MASTER112_PDF,
    power.MASTER148_PDF,
    power.MASTER155_PDF,
]


@utila.saveme
def main():
    bachelor, master, diss, docus, todo = (
        'bachelor' in sys.argv,
        'master' in sys.argv,
        'diss' in sys.argv,
        'docs' in sys.argv,
        'todo' in sys.argv,
    )
    jobs = []
    if bachelor:
        jobs.extend(power.BACHELORS)
    if master:
        jobs.extend(power.MASTERS)
    if diss:
        jobs.extend(power.DISSS)
    if docus:
        jobs.extend(power.DOCUS)
    if todo:
        jobs.extend(TODO)
    if 'all' in sys.argv:
        jobs = power.PDF
        utila.log(f'publish all docs: {len(jobs)}')
    for path in jobs:
        utila.log(f'upload: {path}')
        train.performance.upload(path, port=train.DEV_SERVER_PORT, public=True)
    utila.log('done')
    sys.exit(utila.SUCCESS)
