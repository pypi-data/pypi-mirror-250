# -*- coding: utf-8 -*-

import typing as T
import json
import dataclasses
from datetime import datetime

import botocore.exceptions

from ..base import (
    T_ID,
    BaseTracker,
    T_TRACKER,
)

if T.TYPE_CHECKING:  # pragma: no cover
    from mypy_boto3_s3 import S3Client


@dataclasses.dataclass
class S3Tracker(BaseTracker):
    """
    This Tracker uses AWS S3 as the backend.
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
    def get_bucket_key(self, id: T_ID) -> T.Tuple[str, str]:
        """
        The path of the tracker file.
        """
        raise NotImplementedError

    @classmethod
    def get_s3_client(cls) -> "S3Client":
        """
        Get the s3 client.
        """
        raise NotImplementedError

    @classmethod
    def load(cls, id: T_ID, **kwargs) -> T.Optional["T_TRACKER"]:
        """
        Create a tracker object by loading from the backend. If not found, return None.
        """
        bucket, key = cls.get_bucket_key(id)
        s3_client = cls.get_s3_client()
        try:
            res = s3_client.get_object(Bucket=bucket, Key=key)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                return None
            else:  # pragma: no cover
                raise e

        data = json.loads(res["Body"].read().decode("utf-8"))
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
        bucket, key = self.get_bucket_key(self.id)
        s3_client = self.get_s3_client()
        s3_client.put_object(Bucket=bucket, Key=key, Body=json.dumps(data, indent=4))
