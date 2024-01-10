# -*- coding: utf-8 -*-

import typing as T
import dataclasses
from pathlib import Path

from ..vendor.better_dataclass import DataClass
from ..records.aws_kinesis import (
    T_KINESIS_RECORD,
    KinesisGetRecordsResponseRecord,
)
from ..consumer import (
    T_POINTER,
    T_CHECK_POINT,
    BaseConsumer,
)

if T.TYPE_CHECKING:
    from boto_session_manager import BotoSesManager


@dataclasses.dataclass
class ShardHashKeyRange(DataClass):
    StartingHashKey: str = dataclasses.field(default=None)
    EndingHashKey: str = dataclasses.field(default=None)


@dataclasses.dataclass
class ShardSequenceNumberRange(DataClass):
    StartingSequenceNumber: str = dataclasses.field(default=None)
    EndingSequenceNumber: str = dataclasses.field(default=None)


@dataclasses.dataclass
class Shard(DataClass):
    # fmt: off
    ShardId: str = dataclasses.field(default=None)
    ParentShardId: T.Optional[str] = dataclasses.field(default=None)
    AdjacentParentShardId: T.Optional[str] = dataclasses.field(default=None)
    HashKeyRange: ShardHashKeyRange = ShardHashKeyRange.nested_field(default_factory=ShardHashKeyRange)
    SequenceNumberRange: ShardSequenceNumberRange = ShardSequenceNumberRange.nested_field(default_factory=ShardSequenceNumberRange)
    # fmt: on

    @classmethod
    def from_list_shards_response(cls, res: dict) -> T.List["Shard"]:
        shards = res.get("Shards", [])
        return [cls.from_dict(shard) for shard in shards]


class ShardIsClosedError(Exception):
    pass


def get_default_backoff_wait_times() -> T.List[int]:
    return [1, 5, 30]


@dataclasses.dataclass
class PocAwsKinesisStreamConsumer(BaseConsumer):
    """
    User can just call :meth:`Consumer.run` method to start consuming. User also
    can explicitly call :meth:`Consumer.get_records`, :meth:`Consumer.process_record` method
     to get records and process record.

    .. note::

        this consumer use a local file to store checkpoint and use a local file as a DLQ.
        this is for POC only, in production, you should use a DynamoDB + S3 for checkpoint,
        and use AWS SQS or another AWS Kinesis Stream for DLQ.
    """

    record_class: T.Type[T_KINESIS_RECORD] = dataclasses.field()
    bsm: "BotoSesManager" = dataclasses.field()
    stream_name: str = dataclasses.field()
    shard_id: str = dataclasses.field()
    path_dlq: Path = dataclasses.field()

    @classmethod
    def new(
        cls,
        record_class: T.Type[T_KINESIS_RECORD],
        consumer_id: str,
        bsm: "BotoSesManager",
        stream_name: str,
        shard_id: str,
        path_dlq: Path,
        checkpoint: T_CHECK_POINT,
        limit: int = 1000,
        exp_backoff_multiplier: int = 1,
        exp_backoff_base: int = 2,
        exp_backoff_min: int = 1,
        exp_backoff_max: int = 0,
        max_retry: int = 4,
        skip_error: bool = True,
        delay: T.Union[int, float] = 0,
    ):
        return cls(
            record_class=record_class,
            consumer_id=consumer_id,
            bsm=bsm,
            stream_name=stream_name,
            shard_id=shard_id,
            path_dlq=path_dlq,
            checkpoint=checkpoint,
            limit=limit,
            exp_backoff_multiplier=exp_backoff_multiplier,
            exp_backoff_base=exp_backoff_base,
            exp_backoff_min=exp_backoff_min,
            exp_backoff_max=exp_backoff_max,
            max_retry=max_retry,
            skip_error=skip_error,
            delay=delay,
        )

    def get_records(
        self,
        limit: T.Optional[int] = None,
    ) -> T.Tuple[T.List[T_KINESIS_RECORD], T_POINTER]:
        """
        Call ``boto3.client("kinesis").get_records(...)`` API to get records.
        """
        if limit is None:
            limit = self.limit
        res = self.bsm.kinesis_client.get_records(
            ShardIterator=self.checkpoint.start_pointer,
            Limit=limit,
        )
        next_pointer = res.get("NextShardIterator")
        response_records = KinesisGetRecordsResponseRecord.from_get_records_response(
            res
        )
        records = [
            self.record_class.from_get_record_data(response_record.data)
            for response_record in response_records
        ]
        return records, next_pointer
