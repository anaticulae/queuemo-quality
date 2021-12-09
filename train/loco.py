# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import os
import subprocess

import utila

Status = collections.namedtuple('Status', 'viewo, queuemo')


class Locomotive:

    def __init__(
        self,
        root: str,
        port: int,
        runtime: int = 1,
        jobs: int = 1,
        verbose: bool = False,
    ):
        self.root = root
        self.port = port
        self.runtime = runtime
        self.jobs = jobs
        self.viewo = None
        self.queuemo = None
        self.verbose = verbose

    def state(self) -> Status:
        viewo = check_process(self.viewo)
        queuemo = check_process(self.queuemo)
        return Status(viewo=viewo, queuemo=queuemo)

    def started(self) -> bool:
        completed = utila.run(
            f'curl http://localhost:{self.port}',
            expect=None,
        )
        return not completed.returncode

    def close(self) -> Status:
        self.viewo.terminate()
        self.queuemo.terminate()

    def start(self):
        assert not self.started(), 'already running'
        assert self.viewo is None and self.queuemo is None

        tmp = os.path.join(self.root, 'tmp')
        os.makedirs(tmp)
        todo = os.path.join(self.root, 'todo')
        os.makedirs(todo)
        ready = os.path.join(self.root, 'ready')
        os.makedirs(ready)

        silent = subprocess.PIPE if not self.verbose else None

        env = dict(os.environ)
        env['SHARED_SPACE'] = str(self.root)
        env['SHARED_TODO'] = str(todo)
        env['SHARED_READY'] = str(ready)
        env['SHARED_TMP'] = str(tmp)

        env['FLASK_APP'] = 'viewo.__main__'

        cmd = f'python -m flask run -p {self.port}'
        # HINT: DO NOT USE WITH TO AVOID WAITING PROBLEM
        # pylint:disable=R1732
        self.viewo = subprocess.Popen(
            cmd,
            env=env,
            stdout=silent,
            stderr=silent,
        )
        # ensure that process is started correctly
        assert check_process(self.viewo) is None
        cmd = f'queuemo --runtime={self.runtime} --jobs={self.jobs}'
        self.queuemo = subprocess.Popen(
            cmd,
            env=env,
            stdout=silent,
            stderr=silent,
        )
        # ensure that process is started correctly
        assert check_process(self.queuemo) is None

    def wait(self, seconds=10) -> Status:
        result = None
        if seconds is None:
            seconds = 3600
        for _ in range(seconds):
            result = self.state()
            if result.queuemo is not None:
                assert result.viewo is None, str(result)
                self.close()
                # update starte
                result = self.state()
                break
        return result


def create(root: str, port: int, runtime: int = 1):
    return Locomotive(
        root=root,
        port=port,
        runtime=runtime,
        verbose=True,
    )


def check_process(process) -> int:
    try:
        outs, errs = process.communicate(timeout=1.0)
        if outs:
            utila.info(outs)
        if errs:
            utila.info(errs)
    except subprocess.TimeoutExpired:
        pass
    return process.returncode
