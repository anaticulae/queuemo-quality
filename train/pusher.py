# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import utilo

import train
import train.performance

try:
    import hardcore  # pylint:disable=E0401
except ModuleNotFoundError:
    hardcore = None  # pylint:disable=C0103


@utilo.saveme
def main():
    args = create()
    jobs = select(args)
    if not jobs:
        utilo.error('nothing todo')
        return utilo.FAILURE
    port = train.DEV_SERVER_PORT
    if args['port']:
        port = int(args['port'])
    host = train.DEV_SERVER_URL
    if args['host']:
        host = args['host']
    upload(
        jobs=jobs,
        port=port,
        host=host,
    )
    return utilo.SUCCESS


def create():
    hoverpowers = utilo.Parameter(
        shortcut='p',
        longcut='hoverpower',
        message='hoverpower files',
    )
    hardcores = utilo.Parameter(
        shortcut='hc',
        longcut='hardcore',
        message='hardcore files',
    )
    commands = [
        hoverpowers,
        hardcores,
        utilo.NumberedParameter(
            shortcut='n',
            longcut='newest',
            message='n newest files',
            default=0,
        ),
        utilo.NumberedParameter(
            shortcut='o',
            longcut='oldest',
            message='n oldest files',
            default=0,
        ),
        utilo.Parameter(
            longcut='host',
            message='server url to publish',
        ),
        utilo.NumberedParameter(
            longcut='port',
            message='server port to publish',
            default=train.DEV_SERVER_PORT,
        ),
    ]
    parser = utilo.create_parser(
        todo=commands,
        config=utilo.ParserConfiguration.all_off(),
        version=train.__version__,
    )
    parser.add_argument(
        'regex',
        nargs='?',
        help='select matching files or a single file.',
    )
    args = utilo.parse(parser)
    return args


def select(args) -> list:
    jobs = []
    if hoverpowers := args.get('hoverpower'):
        pages = utilo.parse_pages(hoverpowers, pagecount=len(hoverpower.PDF))
        if pages is None:
            jobs.extend(hoverpower.PDF)
        else:
            jobs.extend([hoverpower.PDF[page] for page in pages])
    if hardcores := args.get('hardcore'):
        pages = utilo.parse_pages(hardcores, pagecount=len(hardcore.ALL))
        if pages is None:
            jobs.extend(hardcore.ALL)
        else:
            jobs.extend([hardcore.ALL[page] for page in pages])
    if number := args.get('newest'):
        jobs.extend(newest(number))
    if number := args.get('oldest'):
        jobs.extend(oldest(number))
    if regex := args.get('regex'):
        if files := file_select(regex):
            jobs.extend(files)
        else:
            jobs.extend(regex_select(regex=regex))
    return jobs


def regex_select(regex: str) -> list:
    """Select files via regex.

    Use hoverpower and hardcore as source of selection.

    >>> regex_select('bachelor032')
    ['...', '...',...]
    """
    result = [
        item for item in hoverpower.PDF  # + hardcore.ALL # TODO: ENABLE LATER
        if utilo.file_name(item).startswith(regex)
    ]
    return result


def file_select(path: str) -> list:
    """Select file which is not part of corpus(hoverpower, hardcore).

    This file is mostly selected via cli.

    >>> file_select(__file__)
    ['...pusher.py']
    """
    if not utilo.isfilepath(path):
        return None
    return [utilo.make_absolute(path)]


def upload(jobs, port, host):
    utilo.log(f'publish to port: {port}')
    utilo.log(f'publish to host: {host}')
    for path in jobs:
        utilo.log(f'upload: {path}')
        train.performance.upload(
            path,
            server=host,
            port=port,
            public=True,
        )


def newest(count: int = 10) -> list:
    """\
    >>> assert len(newest(10)) == 10
    """
    files = sorted(hoverpower.PDF, key=utilo.file_age)
    result = files[0:count]
    return result


def oldest(count: int = 10) -> list:
    """\
    >>> assert len(oldest(5)) == 5
    """
    files = sorted(hoverpower.PDF, key=utilo.file_age, reverse=True)
    result = files[0:count]
    return result
