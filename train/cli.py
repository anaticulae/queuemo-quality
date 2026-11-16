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

import utilo

import train
import train.loco


@utilo.saveme
def main():
    commands = [
        utilo.NumberedParameter(
            shortcut='p',
            message='used port',
            default=train.DEV_SERVER_PORT,
        ),
        utilo.NumberedParameter(shortcut='r', message='runtime', default=3600),
        utilo.Parameter(longcut='workspace', message='workspace'),
    ]
    parser = utilo.cli.create_parser(
        todo=commands,
        config=utilo.ParserConfiguration(
            multiprocessed=True,
            inputparameter=False,
            outputparameter=False,
            prefix=False,
            verboseflag=True,
        ),
        version=train.__version__,
    )
    args = utilo.parse(parser)

    port = int(args['p'])
    runtime = int(args['r'])
    jobs = int(args['job'])
    workspace = os.getcwd() if args['workspace'] is None else args['workspace']
    if not os.path.exists(workspace):
        utilo.error(f'workspace does not exists: {workspace}')
        sys.exit(utilo.FAILURE)

    loco = train.loco.Locomotive(
        root=workspace,
        port=port,
        runtime=runtime,
        jobs=jobs,
    )
    if loco.started():
        utilo.error(f'server already started: {port} | {workspace}')
        sys.exit(utilo.FAILURE)

    loco.start()
    loco.wait(runtime)
    sys.exit(utilo.SUCCESS)
