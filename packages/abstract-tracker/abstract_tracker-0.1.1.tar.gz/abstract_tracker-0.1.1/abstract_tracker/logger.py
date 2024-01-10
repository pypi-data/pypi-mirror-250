# -*- coding: utf-8 -*-

from .vendor.nested_logger import NestedLogger

logger = NestedLogger(
    name="abstract_tracker",
    log_format="%(message)s",
)
