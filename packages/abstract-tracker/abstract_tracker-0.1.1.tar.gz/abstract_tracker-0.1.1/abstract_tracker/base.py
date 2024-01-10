# -*- coding: utf-8 -*-

"""
This module implements the abstraction layer of a :class:`BaseTracker`.
"""

import typing as T
import uuid
import traceback
import contextlib
from datetime import datetime, timezone, timedelta

from .vendor.better_enum import BetterIntEnum

from .exc import TaskLockedError, NoMoreRetryError
from .logger import logger

EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc)


def get_utc_now() -> datetime:
    """
    Get time aware utc now datetime object.
    """
    return datetime.utcnow().replace(tzinfo=timezone.utc)


class BaseStatusEnum(BetterIntEnum):
    pass


class StatusEnum(BaseStatusEnum):
    pending = 0  # 📅
    in_progress = 10  # ⏳
    failed = 20  # ❌
    exhausted = 30  # 🚫
    succeeded = 40  # ✅
    ignored = 50  # 🙅


T_STATUS_ENUM = T.TypeVar("T_STATUS_ENUM", bound=StatusEnum)

T_ID = T.Union[str, int]


class BaseTracker:
    """
    Tracker is a metadata container to track the processing status of a task.

    It should have the following features:

    - be able to track the status of a task
    - provide a lock mechanism to prevent multiple workers from processing
        the same task at the same time
    - provide a retry and exhaustion mechanism to prevent the task
        from being processed indefinitely.
    - be able to capture the error information of the task for debugging

    You can use any framework to implement the tracker subclass, for instance:

    - `dataclasses <https://docs.python.org/3/library/dataclasses.html>`_
    - `attrs <https://www.attrs.org/>`_
    - `pydantic <https://github.com/pydantic/pydantic>`_
    - `Sqlalchemy <https://docs.sqlalchemy.org/en/20/orm/quickstart.html>`_
    - `Django <https://docs.djangoproject.com/en/5.0/topics/db/models/>`_
    - `pynamodb <https://pynamodb.readthedocs.io/>`_

    :param id: The unique identifier of the tracker.
        Usually, it's the same as the task id.
    :param status: Indicate the status of the tracker.
    :param create_time: when the tracker is created.
        Usually, it's the time a task is scheduled as to do.
    :param update_time: when the tracker status is updated.
    :param attempts: how many times we have tried to process the tracker.
    :param lock: a concurrency control mechanism. It is an uuid string.
        if the worker has the same lock as the tracker, it can process the tracker
        even it is locked.
    :param lock_time: when this tracker is locked. so other workers can't work on it.
    :param lock_expire_time: when this lock will expire.
    :param data: arbitrary data in python dictionary.
    :param errors: arbitrary error data in python dictionary.
    """

    id: T_ID
    status: int
    attempts: int
    create_time: datetime
    update_time: datetime
    lock: T.Optional[str]
    lock_time: T.Optional[datetime]
    lock_expire_time: T.Optional[datetime]
    data: dict
    errors: dict

    # --------------------------------------------------------------------------
    # Class Attribute
    #
    # Class attributes is bound to the class, not the instance.
    # We should not use the following syntax to declare that, it may interrupt
    # the class declaration if you are using ORM. Also, it is bad to store a
    # mutable object as class attribute in this way.
    #
    # class MyClass
    #     my_class_attribute: int = 1
    #
    # We should use classmethod to present class attribute.
    # --------------------------------------------------------------------------
    @classmethod
    def get_status_enum(cls) -> T.Type[T_STATUS_ENUM]:  # pragma: no cover
        """
        The :class:`StatusEnum` or a subclass bound to this tracker.
        """
        return StatusEnum

    @classmethod
    def get_expire(cls) -> int:  # pragma: no cover
        """
        Number of seconds before a lock expires for this tracker.
        """
        return 900  # 15 minutes

    @classmethod
    def get_max_attempts(cls) -> int:  # pragma: no cover
        """
        Maximum number of attempts before this task is considered exhaused.
        """
        return 3

    @classmethod
    def new(
        cls,
        id: T_ID,
    ) -> "T_TRACKER":
        """ """
        now = get_utc_now()
        obj = cls(
            id=id,
            status=cls.get_status_enum().pending.value,
            attempts=0,
            create_time=now,
            update_time=now,
            lock=None,
            lock_time=EPOCH,
            lock_expire_time=EPOCH,
            data={},
            errors={},
        )
        obj.dump()
        return obj

    # --------------------------------------------------------------------------
    # Abstract method
    #
    # Abstract methods are intentionally left not implemented. The subclass of
    # different backend should implement these methods.
    # --------------------------------------------------------------------------
    @classmethod
    def load(cls, id: str, **kwargs) -> T.Optional["T_TRACKER"]:
        """
        Create a tracker object by loading from the backend. If not found, return None.
        """
        raise NotImplementedError

    def dump(self, **kwargs):
        """
        Write the tracker object to the backend.
        """
        raise NotImplementedError

    # --------------------------------------------------------------------------
    # Tracker logic methods
    #
    # Tracker logic methods defines the common operations like lock, unlock,
    # update status, etc.
    # --------------------------------------------------------------------------
    @property
    def status_name(self) -> str:  # pragma: no cover
        """
        Get the human friendly name of the status.
        """
        return self.get_status_enum().get_by_value(self.status).name

    def lock_it(
        self,
        now: T.Optional[datetime] = None,
        expire_time: T.Optional[datetime] = None,
    ):
        """
        Lock the tracker.

        .. note::

            This method will NOT dump the tracker data to backend.
        """
        if now is None:
            now = get_utc_now()
        if expire_time is None:
            expire_time = now + timedelta(seconds=self.get_expire())
        if now >= expire_time:  # pragma: no cover
            raise ValueError("expire_time must be in the future")
        self.lock = uuid.uuid4().hex
        self.lock_time = now
        self.lock_expire_time = expire_time

    def unlock_it(self):
        """
        Unlock the tracker.

        .. note::

            This method will NOT dump the tracker data to backend.
        """
        self.lock = None

    def is_locked(
        self,
        lock: T.Optional[str] = None,
        now: T.Optional[datetime] = None,
    ) -> bool:
        """
        Check if the tracker is locked.

        If the ``self.lock`` is None, then consider it is not locked.
        If the ``self.lock`` is not None, then compare it to the manually provided
        ``lock`` parameter. If they are the same, then consider it is not locked.
        Otherwise, check if the lock is expired.

        :param lock: the lock to compare with ``self.lock``.
        :param now: the current time. If not provided, use ``get_utc_now()``.
        """
        if self.lock is None:
            return False
        if self.lock == lock:
            return False
        if now is None:
            now = get_utc_now()
        return now < self.lock_expire_time

    def mark_as_in_progress(
        self,
        now: T.Optional[datetime] = None,
        expire: T.Optional[int] = None,
    ):
        """
        Mark the tracker as in progress.
        """
        status = self.get_status_enum().in_progress.value
        logger.info(f"set status = {status!r} (⏳ in_progress) and 🔓 lock the task.")
        if now is None:
            now = get_utc_now()
        if expire is None:
            expire = self.get_expire()
        expire_time = now + timedelta(seconds=expire)
        self.status = status
        self.attempts += 1
        self.update_time = now
        self.lock_it(
            expire_time=expire_time,
            now=now,
        )
        self.dump()

    def mark_as_failed_or_exhausted(self, e: Exception):
        """
        Mark the tracker as failed or exhausted.
        """
        now = get_utc_now()
        if self.attempts >= self.get_max_attempts():
            self.status = self.get_status_enum().exhausted.value
            logger.info(
                f"❌ task failed {self.attempts} times already, "
                f"set status = {self.status} (🚫 ignored) and 🔐 unlock the task."
            )
        else:
            self.status = self.get_status_enum().failed.value
            logger.info(
                f"❌ task failed, "
                f"set status = {self.status} (❌ failed) and 🔐 unlock the task."
            )
        self.update_time = now
        self.unlock_it()
        self.errors = {
            "error": repr(e),
            "traceback": traceback.format_exc(limit=10),
        }
        self.dump()

    def mark_as_succeeded(self):
        """
        Mark the tracker as succeeded.
        """
        status = self.get_status_enum().succeeded.value
        logger.info(
            f"task succeeded, set status = {status!r} (✅ succeeded) and 🔐 unlock the task."
        )
        now = get_utc_now()
        self.status = status
        self.update_time = now
        self.unlock_it()
        self.dump()

    @contextlib.contextmanager
    def start(
        self,
        lock: T.Optional[str] = None,
        now: T.Optional[datetime] = None,
        expire: T.Optional[int] = None,
        ignore_lock: bool = False,
        force_execution: bool = False,
        verbose: bool = False,
    ):
        """
        A context manager to execute a task, and handle error automatically.

        1. It will set the status to ``in_progress`` and set the lock.
            If the task is already locked, it will raise a :class:`TaskLockedError`.
        2. If the task succeeded, it will set the status to the ``success``.
        3. If the task fail, it will set the status to the ``failed`` and
            log the error to ``errors`` attribute.
        4. If the task failed N times in a row, it will set the status to the
            ``exhausted``.

        :param lock: see :meth:`~BaseTracker.is_locked`
        :param now: the current time. If not provided, use ``get_utc_now()``.
        :param expire: the lock expire time in seconds. If not provided, use
            :meth:`~BaseTracker.get_expire``.
        :param ignore_lock: if True, ignore the lock and execute the task anyway.
        :param force_execution: if True, force to execute even the current status
            is exhausted or ignored.
        """
        if verbose is False:
            existing_handlers = list(logger._logger.handlers)
            logger._logger.handlers.clear()

        status_enum = self.get_status_enum()
        status_name = status_enum.get_by_value(self.status).name
        logger.ruler(
            f"⏱ ⏩ start task(id={self.id!r}, status={self.status!r} ({status_name}), attempts={self.attempts+1})",
        )

        if self.is_locked(lock=lock, now=now):
            if ignore_lock is False:
                logger.info(f"🔓 the task is locked, do nothing!")
                logger.ruler(f"⏰ ⏹️ end task(id={self.id!r} status={self.status!r}))")
                raise TaskLockedError(f"Task {self.id} is locked.")

        if self.status == status_enum.exhausted.value:
            if force_execution is False:
                logger.info(f"the task is 🚫 exhausted, do nothing!")
                logger.ruler(f"⏰ ⏹️ end task(id={self.id!r} status={self.status!r}))")
                raise NoMoreRetryError(
                    f"Already tried {self.attempts} times, No more retry for task {self.id}."
                )

        if self.status == status_enum.ignored.value:  # pragma: no cover
            if force_execution is False:
                logger.info(f"the task is 🙅 ignored, do nothing!")
                logger.ruler(f"⏰ ⏹️ end task(id={self.id!r} status={self.status!r}))")
                raise NoMoreRetryError(
                    f"This task is ignored, No more retry for task {self.id}."
                )

        # the tracker system may also fail, we need to handle it.
        self.mark_as_in_progress(now=now, expire=expire)

        try:
            error = None
            logger._nested_start(pipe="⏳")
            logger.ruler("start task logging")
            yield self

            logger.ruler("end task logging")
            logger._nested_end()
            self.mark_as_succeeded()
        except Exception as e:
            logger.ruler("end task logging")
            logger._nested_end()
            self.mark_as_failed_or_exhausted(e)
            error = e
        finally:
            logger.ruler(f"⏰ ⏹️ end task(id={self.id!r} status={self.status!r}))")
            if verbose is False:
                for handler in existing_handlers:
                    logger._logger.handlers.append(handler)
            if error is not None:
                raise error


T_TRACKER = T.TypeVar("T_TRACKER", bound=BaseTracker)
