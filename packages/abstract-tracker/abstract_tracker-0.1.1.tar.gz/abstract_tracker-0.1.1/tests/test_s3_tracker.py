# -*- coding: utf-8 -*-

import time
import random
import dataclasses

import boto3
import moto

from abstract_tracker.logger import logger
from abstract_tracker.base import StatusEnum
from abstract_tracker.trackers.s3_tracker import T_ID, S3Tracker
from abstract_tracker.tests.mock_aws import BaseMockTest

from abstract_tracker.tests.task import (
    TaskError,
    run_good_task,
    run_bad_task,
    run_random_error_task,
)

bucket = "my-bucket"


@dataclasses.dataclass
class MyTracker(S3Tracker):
    @classmethod
    def get_bucket_key(self, id: T_ID):
        return bucket, f"{id}.json"

    @classmethod
    def get_s3_client(cls):
        return boto3.client("s3")

    @classmethod
    def get_max_attempts(cls) -> int:
        return 10


class TestS3Tracker(BaseMockTest):
    mock_list = [
        moto.mock_sts,
        moto.mock_s3,
    ]
    s3_client = None

    @classmethod
    def setup_class_post_hook(cls):
        cls.s3_client = boto3.client("s3")
        cls.s3_client.create_bucket(Bucket=bucket)

    def test(self):
        assert MyTracker.load(id=1) is None

        MyTracker.new(id=1)
        for _ in range(15):
            time.sleep(0.1)
            tracker = MyTracker.load(id=1)
            if tracker.status == StatusEnum.succeeded.value:
                break
            try:
                with tracker.start(verbose=False):
                    run_random_error_task()
            except TaskError:
                pass


if __name__ == "__main__":
    from abstract_tracker.tests import run_cov_test

    run_cov_test(__file__, "abstract_tracker.trackers.s3_tracker", preview=False)
