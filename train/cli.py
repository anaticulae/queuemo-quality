# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila

import train
import train.loco


@utila.saveme
def main():
    # yapf:disable
    commands = [
        utila.NumberedParameter(shortcut='p', message='used port', default=5000),
        utila.NumberedParameter(shortcut='r', message='runtime', default=3600),
        utila.NumberedParameter(shortcut='j', message='jobs', default=1000),
        utila.Parameter(longcut='workspace', message='workspace'),
    ]
    # yapf:enable
    parser = utila.cli.create_parser(
        todo=commands,
        config=utila.ParserConfiguration(
            outputparameter=False,
            inputparameter=False,
            prefix=False,
            verboseflag=True,
        ),
        version=train.__version__,
    )
    args = utila.parse(parser)

    port = int(args['p'])
    runtime = int(args['r'])
    jobs = int(args['j'])
    workspace = os.getcwd() if args['workspace'] is None else args['workspace']
    if not os.path.exists(workspace):
        utila.error(f'workspace does not exists: {workspace}')
        exit(utila.FAILURE)

    loco = train.loco.Locomotive(
        root=workspace,
        viewo_port=port,
        runtime=runtime,
        jobs=jobs,
    )
    if loco.started():
        utila.error(f'server already started: {port} | {workspace}')
        exit(utila.FAILURE)

    loco.start()
    loco.wait(runtime)
    exit(utila.SUCCESS)
