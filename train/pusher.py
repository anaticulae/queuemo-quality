# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re
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
    argv = sys.argv
    jobs = []
    jobs.extend(select_doctype(argv))
    jobs.extend(select_single(argv))
    if 'all' in sys.argv:
        jobs = power.PDF
        utila.log(f'publish all docs: {len(jobs)}')
    upload(jobs)
    utila.log('done')
    sys.exit(utila.SUCCESS)


SINGLE = re.compile(r'\w+\d{3}')


def select_single(argv):
    jobs = []
    singles = [SINGLE.search(str(item)) for item in argv]
    singles = utila.notnone(singles)
    singles = [utila.extract_match(item) for item in singles]
    jobs = [item for item in power.PDF if any(it in item for it in singles)]
    return jobs


def select_doctype(argv):
    bachelor, master, diss, docus, paper, todo = (
        'bachelor' in argv,
        'master' in argv,
        'diss' in argv,
        'docu' in argv,
        'paper' in argv,
        'todo' in argv,
    )
    minimal = 'minimal' in argv
    jobs = []
    for resources, selected in zip(
        (
            power.BACHELORS,
            power.MASTERS,
            power.DISSS,
            power.DOCUS,
            power.PAPERS,
            TODO,
        ),
        (
            bachelor,
            master,
            diss,
            docus,
            paper,
            todo,
        ),
    ):
        if not selected:
            continue
        if minimal:
            jobs.extend(resources[0:10])
        else:
            jobs.extend(resources)
    return jobs


def upload(jobs):
    for path in jobs:
        utila.log(f'upload: {path}')
        train.performance.upload(path, port=train.DEV_SERVER_PORT, public=True)
