# -*- coding: utf-8 -*-

import shutil
import random
import dataclasses
from pathlib import Path

import pytest

from abstract_tracker.logger import logger
from abstract_tracker.exc import TaskLockedError
from abstract_tracker.base import StatusEnum, NoMoreRetryError
from abstract_tracker.trackers.file_tracker import T_ID, FileTracker
from abstract_tracker.tests.task import (
    TaskError,
    run_good_task,
    run_bad_task,
    run_random_error_task,
)

dir_data = Path(__file__).parent / "file_tracker"
shutil.rmtree(dir_data, ignore_errors=True)
dir_data.mkdir(parents=True, exist_ok=True)


@dataclasses.dataclass
class MyTracker(FileTracker):
    @classmethod
    def get_path(cls, id: T_ID) -> Path:
        return dir_data.joinpath(f"{id}.json")

    @classmethod
    def get_expire(cls) -> int:
        return 5

    @classmethod
    def get_max_attempts(cls) -> int:
        return 2


def _test_run_good_task():
    """
    It may succeed or dead.
    """
    assert MyTracker.load(id=1) is None

    tracker = MyTracker.new(id=1)
    with tracker.start(verbose=True):
        run_good_task()
    assert tracker.status == StatusEnum.succeeded.value
    assert tracker.attempts == 1
    assert tracker.lock is None


def _test_run_bad_task():
    """
    It may succeed or dead.
    """
    assert MyTracker.load(id=2) is None

    # the first attempt fail
    tracker = MyTracker.new(id=2)
    with pytest.raises(TaskError):
        with tracker.start(verbose=True):
            run_bad_task()
    assert tracker.status == StatusEnum.failed.value
    assert tracker.attempts == 1
    assert tracker.lock is None

    # failed the second time, now it's exhausted
    tracker = MyTracker.load(id=2)
    with pytest.raises(TaskError):
        with tracker.start(verbose=True):
            run_bad_task()
    assert tracker.status == StatusEnum.exhausted.value
    assert tracker.attempts == 2
    assert tracker.lock is None

    # now it's exhausted, do nothing
    tracker = MyTracker.load(id=2)
    with pytest.raises(NoMoreRetryError):
        with tracker.start(verbose=True):
            run_bad_task()

    # force execution
    tracker = MyTracker.load(id=2)
    with tracker.start(force_execution=True, verbose=True):
        run_good_task()
    assert tracker.status == StatusEnum.succeeded.value
    assert tracker.attempts == 3
    assert tracker.lock is None


def _test_lock():
    # first time, we lock it
    tracker = MyTracker.new(id=3)
    tracker.status = StatusEnum.in_progress.value
    tracker.lock_it()
    tracker.dump()
    assert tracker.status == StatusEnum.in_progress.value
    assert tracker.lock is not None
    lock = tracker.lock

    # another worker try to run it, but it's locked
    tracker = MyTracker.load(id=3)
    assert tracker.is_locked() is True
    assert tracker.is_locked(lock=lock) is False

    with pytest.raises(TaskLockedError):
        with tracker.start(verbose=True):
            run_good_task()
    tracker = MyTracker.load(id=3)
    assert tracker.is_locked() is True

    # another work ignore the lock and run it
    with tracker.start(ignore_lock=True, verbose=True):
        run_good_task()
    assert tracker.status == StatusEnum.succeeded.value
    assert tracker.is_locked() is False


def _test_verbose():
    tracker = MyTracker.new(id=4)
    with tracker.start(verbose=False):
        run_good_task()

    with tracker.start(verbose=True):
        run_good_task()


def test():
    print("")
    with logger.disabled(
        disable=True,  # no log
        # disable=False,  # has log
    ):
        _test_run_good_task()
        _test_run_bad_task()
        _test_lock()
        _test_verbose()


if __name__ == "__main__":
    from abstract_tracker.tests import run_cov_test

    # run_cov_test(__file__, "abstract_tracker.base", preview=False)
    run_cov_test(__file__, "abstract_tracker.trackers.file_tracker", preview=False)
