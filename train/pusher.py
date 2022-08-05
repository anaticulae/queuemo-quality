# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hardcore
import power
import utila

import train
import train.performance


@utila.saveme
def main():
    args = create()
    jobs = select(args)
    if not jobs:
        utila.error('nothing todo')
        return utila.FAILURE
    port = args.get('port')
    upload(jobs=jobs, port=port)
    return utila.SUCCESS


def create():
    powers = utila.Parameter(
        shortcut='p',
        longcut='power',
        message='power files',
    )
    hardcores = utila.Parameter(
        shortcut='hc',
        longcut='hardcore',
        message='hardcore files',
    )
    commands = [
        powers,
        hardcores,
        utila.NumberedParameter(
            shortcut='n',
            longcut='newest',
            message='n newest files',
            default=0,
        ),
        utila.NumberedParameter(
            shortcut='o',
            longcut='oldest',
            message='n oldest files',
            default=0,
        ),
        utila.NumberedParameter(
            longcut='port',
            message='server to publish',
            default=train.DEV_SERVER_PORT,
        ),
    ]
    parser = utila.create_parser(
        todo=commands,
        config=utila.ParserConfiguration.all_off(),
        version=train.__version__,
    )
    parser.add_argument('regex', nargs='?', help='select matching files')
    args = utila.parse(parser)
    return args


def select(args) -> list:
    jobs = []
    if powers := args.get('power'):
        pages = utila.parse_pages(powers, pagecount=len(power.PDF))
        if pages is None:
            jobs.extend(power.PDF)
        else:
            jobs.extend([power.PDF[page] for page in pages])
    if hardcores := args.get('hardcore'):
        pages = utila.parse_pages(hardcores, pagecount=len(hardcore.ALL))
        if pages is None:
            jobs.extend(hardcore.ALL)
        else:
            jobs.extend([hardcore.ALL[page] for page in pages])
    if number := args.get('newest'):
        jobs.extend(newest(number))
    if number := args.get('oldest'):
        jobs.extend(oldest(number))
    if regex := args.get('regex'):
        jobs.extend(regex_select(regex=regex))
    return jobs


def regex_select(regex: str) -> list:
    """Select files via regex.

    Use power and hardcore as source of selection.

    >>> regex_select('bachelor032')
    ['...', '...',...]
    """
    result = [
        item for item in power.RESOURCES + hardcore.ALL
        if utila.file_name(item).startswith(regex)
    ]
    return result


def upload(jobs, port):
    utila.log(f'publish to port: {port}')
    for path in jobs:
        utila.log(f'upload: {path}')
        train.performance.upload(
            path,
            port=port,
            public=True,
        )


def newest(count: int = 10) -> list:
    """\
    >>> assert len(newest(10)) == 10
    """
    files = sorted(power.PDF, key=utila.file_age)
    result = files[0:count]
    return result


def oldest(count: int = 10) -> list:
    """\
    >>> assert len(oldest(5)) == 5
    """
    files = sorted(power.PDF, key=utila.file_age, reverse=True)
    result = files[0:count]
    return result
