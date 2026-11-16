# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import sys

import configos
import hoverpower
import protoerror
import utilo

import train
import train.performance

FIRST = [
    hoverpower.MASTER098_PDF,
    hoverpower.MASTER116_PDF,
    hoverpower.BACHELOR090_PDF,
    hoverpower.HOME025_PDF,
]

SECOND = [
    hoverpower.MASTER110_PDF,
    hoverpower.BACHELOR128_PDF,
    hoverpower.MASTER031_PDF,
    hoverpower.BACHELOR051_PDF,
]

THIRD = [
    hoverpower.MASTER072_PDF,
    hoverpower.MASTER089_PDF,
    hoverpower.MASTER098_PDF,
    hoverpower.MASTER099_PDF,
]


@utilo.saveme
def main():
    commands = [
        utilo.Flag(longcut='first'),
        utilo.Flag(longcut='second'),
        utilo.Flag(longcut='third'),
    ]
    parser = utilo.cli.create_parser(
        todo=commands,
        config=utilo.ParserConfiguration(
            outputparameter=False,
            inputparameter=False,
            prefix=False,
            verboseflag=True,
        ),
        description='Determine performance for selected pdf package.',
        version=train.__version__,
    )
    args = utilo.parse(parser)

    first = args.get('first', False)
    second = args.get('second', False)
    third = args.get('third', False)

    if first:
        run(FIRST, start=4700)

    if second:
        run(SECOND, start=4710)

    if third:
        run(THIRD, start=4720)

    if not any((first, second, third)):
        parser.print_usage()
        sys.exit(utilo.FAILURE)
    sys.exit(utilo.SUCCESS)


def run(todo, start: int = 4700):
    for port, path in enumerate(todo, start=start):
        workspace = utilo.tmpdir(configos.tmp())
        utilo.log(f'run performance for {path} in {workspace} on: {port}')
        with utilo.profile(path):
            ready = train.performance.run(workspace, path, port=port)
        # load findings by page
        findings = protoerror.findings_from_path(ready)
        # global finding list
        findings = utilo.flat([item.content for item in findings])
        # TODO: REPLACE AFTER UPGRADING?
        findings = utilo.unique(findings)
        utilo.log(f'findings: {len(findings)}')
