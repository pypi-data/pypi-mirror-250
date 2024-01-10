# -*- coding: utf-8 -*-

from abstract_tracker import api


def test():
    _ = api
    _ = api.logger
    _ = api.TaskLockedError
    _ = api.NoMoreRetryError
    _ = api.TaskExhaustedError
    _ = api.TaskIgnoredError
    _ = api.StatusEnum
    _ = api.T_STATUS_ENUM
    _ = api.T_ID
    _ = api.BaseTracker
    _ = api.T_TRACKER
    _ = api.FileTracker
    _ = api.S3Tracker

if __name__ == "__main__":
    from abstract_tracker.tests import run_cov_test

    run_cov_test(__file__, "abstract_tracker.api", preview=False)
