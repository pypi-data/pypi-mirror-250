# -*- coding: utf-8 -*-

"""
Usage example::

    import abstract_tracker.api as abstract_tracker
"""

from .logger import logger
from .exc import TaskLockedError
from .exc import NoMoreRetryError
from .exc import TaskExhaustedError
from .exc import TaskIgnoredError
from .base import StatusEnum
from .base import T_STATUS_ENUM
from .base import T_ID
from .base import BaseTracker
from .base import T_TRACKER
from .trackers.file_tracker import FileTracker

try:
    from .trackers.s3_tracker import S3Tracker
except ImportError:
    pass
