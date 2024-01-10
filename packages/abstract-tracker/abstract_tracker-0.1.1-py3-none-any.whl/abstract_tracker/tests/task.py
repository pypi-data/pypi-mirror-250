# -*- coding: utf-8 -*-

import random
from ..logger import logger


class TaskError(Exception):
    pass


def run_good_task():  # always succeed
    logger.info("running good task")


def run_bad_task():  # always fail
    logger.info("running bad task")
    raise TaskError("task error")


def run_random_error_task():
    logger.info("running random error task")
    if random.randint(1, 100) <= 50:
        raise TaskError("random error")
