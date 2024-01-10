# -*- coding: utf-8 -*-

"""
[CN] 开发者设计文档

This section is for this project maintainer only.

这个模块实现了 Consumer 的基类 :class:`BaseConsumer`. 它实现的功能主要是如何读写 checkpoint,
如何处理在消费 record 中的异常. 它假设你的 stream system 可以是任何系统.

:class:`BaseConsumer` 的子类是一些跟某些特定的 stream system 对接的 Consumer 的具体实现.
它们假设你可以用任何逻辑来消费 record. 它只是负责实现了 :meth:`BaseConsumer.get_records` 方法.
"""

import typing as T
import time
import dataclasses
from datetime import datetime

from tenacity import retry, wait_exponential, stop_after_attempt, RetryError
from .vendor.better_enum import BetterIntEnum

from .exc import StreamIsClosedError
from .utils import get_utc_now
from .logger import logger
from .abstraction import T_RECORD, AbcConsumer


class StatusEnum(BetterIntEnum):
    """
    For each record, we track its processing status, which can be one of the following:

    - pending: the record is not processed ever yet.
    - in_progress: the record is being processed; the processing has started,
        but it has not finished yet. It could fail, but the program has not
        had a chance to mark it as failed.
    - failed: the record has been processed but has failed. It is open for further retry."
    - dead: the record has been processed but has failed too many times.
        we don't want to retry it anymore.
    - succeeded: the record has been processed and has succeeded.
    - ignored: the record is ignored by the consumer. We don't want to process it.
    """

    pending = 0
    in_progress = 20
    failed = 40
    dead = 60
    succeeded = 80
    ignored = 100


@dataclasses.dataclass
class Tracker:
    """
    The Tracker tracks the processing status of **each** record.

    :param record_id: the unique id of the record.
    :param update_at: the timestamp when the record's status is updated.
    :param status: the status of the record's processing.
    :param attempts: the number of times we have tried to process this record.
    :param error: last error message when we tried to process this record.
        None means no error.
    """

    record_id: str = dataclasses.field()
    update_at: str = dataclasses.field()
    status: int = dataclasses.field()
    attempts: int = dataclasses.field()
    error: T.Optional[str] = dataclasses.field(default=None)

    @property
    def update_at_datetime(self) -> datetime:
        """
        The datetime version of the `update_at` field.
        """
        return datetime.fromisoformat(self.update_at)

    @classmethod
    def from_dict(cls, data: dict):
        """
        Serialize the Tracker object to a dict.
        """
        return cls(**data)

    def to_dict(self) -> dict:
        """
        Deserialize the Tracker object from a dict.
        """
        return dataclasses.asdict(self)


T_POINTER = T.Union[str, int]


@dataclasses.dataclass
class CheckPoint:
    """
    CheckPoint stores the processing status, processing metadata and the origin
    records data. It is used to ensure data integrity and exactly-once processing.

    This class manages the data manipulation part of the logics. It intentionally
    leaves the data persistence part NOT implemented. It is up to the developer
    to subclass this class and implement the persistence layer. You can use
    any backend for checkpoint data persistence. For example, you can use
    a file, a database like AWS DynamoDB, or cloud storage like AWS S3.

    :param initial_pointer: the initial pointer to start reading the records.
    :param start_pointer: the start pointer to read a batch of records.
    :param next_pointer: the start pointer to read the next batch of records.
    :param batch_sequence: the nth batch of records we are processing.
    :param batch: the per-record status tracking data for the current batch.
    """

    initial_pointer: T_POINTER = dataclasses.field()
    start_pointer: T_POINTER = dataclasses.field()
    next_pointer: T.Optional[T_POINTER] = dataclasses.field()
    batch_sequence: int = dataclasses.field()
    batch: T.Dict[str, Tracker] = dataclasses.field()

    def to_dict(self) -> dict:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: dict):
        raise NotImplementedError

    def dump(self):
        """
        Dump the checkpoint data to the persistence layer.
        """
        raise NotImplementedError

    @classmethod
    def load(self, **kwargs):
        """
        Load the checkpoint data from the persistence layer.

        It has to handle the edge case that the checkpoint data does not exist.
        """
        raise NotImplementedError

    def dump_records(self, records: T.Iterable[T_RECORD]):
        """
        Dump the records in a batch to the persistence layer.
        """
        raise NotImplementedError

    def load_records(self, record_class: T_RECORD, **kwargs) -> T.Iterable[T_RECORD]:
        """
        Load the batch records from the persistence layer.
        """
        raise NotImplementedError

    def set_record_status(self, record: T_RECORD, status: int):
        """
        Set the status of a record in the batch.
        """
        self.batch[record.id].status = status
        self.batch[record.id].update_at = get_utc_now().isoformat()

    def set_record_as_todo(self, record: T_RECORD):
        self.set_record_status(record, StatusEnum.pending.value)

    def set_record_as_in_progress(self, record: T_RECORD):
        self.set_record_status(record, StatusEnum.in_progress.value)

    def set_record_as_failed(self, record: T_RECORD):
        self.set_record_status(record, StatusEnum.failed.value)

    def set_record_as_dead(self, record: T_RECORD):
        self.set_record_status(record, StatusEnum.dead.value)

    def set_record_as_succeeded(self, record: T_RECORD):
        self.set_record_status(record, StatusEnum.succeeded.value)

    def set_record_as_ignored(self, record: T_RECORD):
        self.set_record_status(record, StatusEnum.ignored.value)

    def is_ready_for_next_batch(self) -> bool:
        """
        Check the processing status for each record in the batch. Check if all records
        reached "finished" status, which means we don't want to retry processing
        any of them anymore. If so, we can move on to the next batch.
        """
        finished_codes = [
            StatusEnum.dead.value,
            StatusEnum.succeeded.value,
            StatusEnum.ignored.value,
        ]
        return all(
            [tracker.status in finished_codes for tracker in self.batch.values()]
        )

    def update_for_new_batch(
        self,
        records: T.List[T_RECORD],
        next_pointer: T.Optional[T_POINTER] = None,
    ):
        """
        Update the checkpoint based on new batch records.

        .. note::

            This method won't persist the checkpoint.
        """
        self.next_pointer = next_pointer
        self.batch_sequence += 1
        self.batch.clear()
        update_at = get_utc_now().isoformat()
        for record in records:
            self.batch[record.id] = Tracker(
                record_id=record.id,
                status=StatusEnum.pending.value,
                attempts=0,
                update_at=update_at,
            )


T_CHECK_POINT = T.TypeVar("T_CHECK_POINT", bound=CheckPoint)


@dataclasses.dataclass
class BaseConsumer(AbcConsumer):
    """
    Consumer continuously fetches batch records from the stream system
    and process them.

    :param record_class: the record class.
    :param consumer_id:
    :param limit:
    :param checkpoint:
    :param exp_backoff_multiplier:
    :param exp_backoff_base:
    :param exp_backoff_min:
    :param exp_backoff_max:
    :param max_retry:
    :param skip_error:
    :param delay:
    """

    record_class: T.Type[T_RECORD] = dataclasses.field()
    consumer_id: str = dataclasses.field()
    limit: int = dataclasses.field()
    checkpoint: T_CHECK_POINT = dataclasses.field()
    exp_backoff_multiplier: int = dataclasses.field()
    exp_backoff_base: int = dataclasses.field()
    exp_backoff_min: int = dataclasses.field()
    exp_backoff_max: int = dataclasses.field()
    max_retry: int = dataclasses.field()
    skip_error: bool = dataclasses.field()
    delay: T.Union[int, float] = dataclasses.field()

    def get_records(
        self,
        limit: int = None,
    ) -> T.Tuple[T.List[T_RECORD], T_POINTER]:
        """
        Get records from the stream system and determine the value of the
        next pointer for the next batch if we successfully process
        this batch of records.

        :param limit: The maximum number of records to return.
        :return: a two-item tuple. the first one is a list of records
            and the second one is the value of the next pointer for the next batch
            if we successfully process this batch of records.

        .. important::

            User has to implement this method.

            If you need additional parameters other than the :class:`BaseConsumer`
            built-in attributes and ``limit``, you should extend this class
            and add the parameters to the subclass.
        """
        raise NotImplementedError

    def process_record(self, record: T_RECORD):
        """
        This method defines how to process a failed record.

        .. important::

            User has to implement this method.
        """
        raise NotImplementedError

    def process_failed_record(self, record: T_RECORD):
        """
        This method defines how to process a failed record.

        .. note::

            By default, it does nothing. In production, you should send
            this record to a dead-letter-queue (DLQ) for further investigation.

            Users can customize this method.
        """
        pass

    def commit(self):
        """
        Mark the current batch has been fully processed.
        """
        if self.checkpoint.next_pointer is None:
            self.checkpoint.dump()
            raise StreamIsClosedError
        else:
            self.checkpoint.start_pointer = self.checkpoint.next_pointer
            self.checkpoint.next_pointer = None
            self.checkpoint.dump()

    def _process_record_with_checkpoint(self, record: T_RECORD):
        """
        A wrapper method of :meth:`BaseConsumer.process_record`,
         process the record and also handle the checkpoint.
        """
        self.checkpoint.set_record_as_in_progress(record)
        self.checkpoint.batch[record.id].attempts += 1
        self.checkpoint.dump()
        try:
            res = self.process_record(record)
            self.checkpoint.set_record_as_succeeded(record)
            self.checkpoint.dump()
            return res
        except Exception as e:
            self.checkpoint.set_record_as_failed(record)
            self.checkpoint.dump()
            raise e

    def _process_record(
        self,
        record: T_RECORD,
    ) -> T.Tuple[T.Optional[bool], T.Any]:
        """

        :return: (bool, typing.Any), where the first element could be True, False or None. True means the record is processed successfully, False means the record the processing is faile, None means the record is not processed. The second element is the :meth:`BaseConsumer.process_record` return value.
        """
        if self.checkpoint.batch[record.id].status not in [
            StatusEnum.pending.value,
            StatusEnum.failed.value,
        ]:
            return None, None

        self.checkpoint.batch[record.id].status = StatusEnum.in_progress.value

        _process_record_with_retry = retry(
            wait=wait_exponential(
                multiplier=self.exp_backoff_multiplier,
                exp_base=self.exp_backoff_base,
                min=self.exp_backoff_min,
                max=self.exp_backoff_max,
            ),
            stop=stop_after_attempt(self.max_retry),
        )(self._process_record_with_checkpoint)

        try:
            res = _process_record_with_retry(record)
            return True, res
        except RetryError as e:
            self.checkpoint.set_record_as_dead(record)
            self.checkpoint.dump()

            _process_failed_record_with_retry = retry(
                wait=wait_exponential(
                    multiplier=self.exp_backoff_multiplier,
                    exp_base=self.exp_backoff_base,
                    min=self.exp_backoff_min,
                    max=self.exp_backoff_max,
                ),
                stop=stop_after_attempt(self.max_retry),
            )(self.process_failed_record)
            res = _process_failed_record_with_retry(record)
            if self.skip_error:
                return False, res
            else:
                e.reraise()

    @logger.emoji_block(
        msg="process batch",
        emoji="⏳",
    )
    def _process_batch(self):
        # check if we should call get_records API
        if self.checkpoint.is_ready_for_next_batch():
            # get records from the stream system
            records, next_pointer = self.get_records()
            # update and persist checkpoint
            self.checkpoint.update_for_new_batch(records, next_pointer)
            self.checkpoint.dump()
            self.checkpoint.dump_records(records)
        else:
            # get records from the checkpoint
            records = self.checkpoint.load_records(record_class=self.record_class)
        # process all record
        for record in records:
            flag, process_record_res = self._process_record(record)
        self.commit()

    def process_batch(
        self,
        verbose: bool = False,
    ):
        with logger.disabled(
            disable=not verbose,
        ):
            return self._process_batch()

    def run(self):
        """
        Run the consumer.
        """
        while 1:
            self._process_batch()
            if self.delay:
                time.sleep(self.delay)
