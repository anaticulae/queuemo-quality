# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import power
import protocol
import utila

import train
import train.performance

FIRST = [
    power.MASTER098_PDF,
    power.MASTER116_PDF,
    power.BACHELOR090_PDF,
    power.HOME025_PDF,
]

SECOND = [
    power.MASTER110_PDF,
    power.BACHELOR128_PDF,
    power.MASTER031_PDF,
    power.BACHELOR051_PDF,
]

THIRD = [
    power.MASTER072_PDF,
    power.MASTER089_PDF,
    power.MASTER098_PDF,
    power.MASTER099_PDF,
]


@utila.saveme
def main():
    commands = [
        utila.Flag(longcut='first'),
        utila.Flag(longcut='second'),
        utila.Flag(longcut='third'),
    ]
    parser = utila.cli.create_parser(
        todo=commands,
        config=utila.ParserConfiguration(
            outputparameter=False,
            inputparameter=False,
            prefix=False,
            verboseflag=True,
        ),
        description='Determine performance for selected pdf package.',
        version=train.__version__,
    )
    args = utila.parse(parser)

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
        exit(utila.FAILURE)
    exit(utila.SUCCESS)


def run(todo, start: int = 4700):
    for port, path in enumerate(todo, start=start):
        workspace = utila.tmpdir(configo.tmp())
        utila.log(f'run performance for {path} in {workspace} on: {port}')
        with utila.profile(path):
            ready = train.performance.run(workspace, path, port=port)
        # load findings by page
        findings = protocol.findings_from_path(ready)
        # global finding list
        findings = utila.flatten([item.content for item in findings])
        # TODO: REPLACE AFTER UPGRADING?
        findings = utila.make_unique(findings)
        utila.log(f'findings: {len(findings)}')
