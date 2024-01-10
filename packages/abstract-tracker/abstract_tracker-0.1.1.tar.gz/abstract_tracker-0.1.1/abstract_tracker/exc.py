# -*- coding: utf-8 -*-


class TaskLockedError(Exception):
    """
    Raised when a task worker is trying to work on a locked task.
    """

    pass


class NoMoreRetryError(Exception):
    """
    Raised when trying to run a task that is considered as no more retry.
    """

    pass


class TaskExhaustedError(NoMoreRetryError):
    """
    Raised when a task is already in "exhausted" status.
    """

    pass


class TaskIgnoredError(NoMoreRetryError):
    """
    Raised when a task is already in "ignore" status.
    """

    pass
