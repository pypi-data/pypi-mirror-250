# -*- coding: utf-8 -*-

import typing as T
import json
import dataclasses
from pathlib import Path
from datetime import datetime

from ..base import (
    T_ID,
    BaseTracker,
    T_TRACKER,
)


@dataclasses.dataclass
class FileTracker(BaseTracker):
    """
    File tracker uses a local json file as the backend.
    """

    id: T_ID = dataclasses.field()
    status: int = dataclasses.field()
    attempts: int = dataclasses.field()
    create_time: datetime = dataclasses.field()
    update_time: datetime = dataclasses.field()
    lock: T.Optional[str] = dataclasses.field()
    lock_time: datetime = dataclasses.field()
    lock_expire_time: datetime = dataclasses.field()
    data: dict = dataclasses.field()
    errors: dict = dataclasses.field()

    @classmethod
    def get_path(self, id: T_ID) -> Path:
        """
        The path of the tracker file.
        """
        raise NotImplementedError

    @property
    def path(self) -> Path:
        """
        The path of the tracker file.
        """
        return self.get_path(self.id)

    @classmethod
    def load(cls, id: T_ID, **kwargs) -> T.Optional["T_TRACKER"]:
        """
        Create a tracker object by loading from the backend. If not found, return None.
        """
        try:
            with cls.get_path(id).open("r") as f:
                data = json.load(f)
                return cls(
                    id=data["id"],
                    status=data["status"],
                    attempts=data["attempts"],
                    create_time=datetime.fromisoformat(data["create_time"]),
                    update_time=datetime.fromisoformat(data["update_time"]),
                    lock=data["lock"],
                    lock_time=datetime.fromisoformat(data["lock_time"]),
                    lock_expire_time=datetime.fromisoformat(data["lock_expire_time"]),
                    data=data["data"],
                    errors=data["errors"],
                )
        except FileNotFoundError:
            return None

    def dump(self, **kwargs):
        """
        Write the tracker object to the backend.
        """
        data = dict(
            id=self.id,
            status=self.status,
            attempts=self.attempts,
            create_time=self.create_time.isoformat(),
            update_time=self.update_time.isoformat(),
            lock=self.lock,
            lock_time=self.lock_time.isoformat(),
            lock_expire_time=self.lock_expire_time.isoformat(),
            data=self.data,
            errors=self.errors,
        )
        with self.path.open("w") as f:
            json.dump(data, f, indent=4)
