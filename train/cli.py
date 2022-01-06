# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import sys

import utila

import train
import train.loco


@utila.saveme
def main():
    commands = [
        utila.NumberedParameter(
            shortcut='p',
            message='used port',
            default=train.DEV_SERVER_PORT,
        ),
        utila.NumberedParameter(shortcut='r', message='runtime', default=3600),
        utila.Parameter(longcut='workspace', message='workspace'),
    ]
    parser = utila.cli.create_parser(
        todo=commands,
        config=utila.ParserConfiguration(
            multiprocessed=True,
            inputparameter=False,
            outputparameter=False,
            prefix=False,
            verboseflag=True,
        ),
        version=train.__version__,
    )
    args = utila.parse(parser)

    port = int(args['p'])
    runtime = int(args['r'])
    jobs = int(args['job'])
    workspace = os.getcwd() if args['workspace'] is None else args['workspace']
    if not os.path.exists(workspace):
        utila.error(f'workspace does not exists: {workspace}')
        sys.exit(utila.FAILURE)

    loco = train.loco.Locomotive(
        root=workspace,
        port=port,
        runtime=runtime,
        jobs=jobs,
    )
    if loco.started():
        utila.error(f'server already started: {port} | {workspace}')
        sys.exit(utila.FAILURE)

    loco.start()
    loco.wait(runtime)
    sys.exit(utila.SUCCESS)
