# -*- coding: utf-8 -*-

"""
[CN] 开发者设计文档

This section is for this project maintainer only.

这个模块描述了几个重要概念的抽象. 它们包括 :class:`AbcRecord`, :class:`AbcBuffer`,
:class:`AbcProducer`, :class:`AbcConsumer`.
"""

import typing as T
import abc
from datetime import datetime


class AbcRecord(abc.ABC):
    """
    Abstract class for a record that should be sent to a target system.

    It should have the following attributes:

    - id: unique identifier for the record.
    - create_at: the ISO8601 representation of the creation time of the record.
        it has to be timezone aware.

    And also the following methods:

    - :meth:`AbcRecord.create_at_dt`
    - :meth:`AbcRecord.serialize`
    - :meth:`AbcRecord.deserialize`
    """

    id: str
    create_at: str

    @property
    def create_at_datetime(self) -> datetime:
        """
        Return the datetime object of the creation time of the record.
        """
        return datetime.fromisoformat(self.create_at)

    @abc.abstractmethod
    def serialize(self) -> str:
        """
        Serialize the record to a string.
        """
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def deserialize(cls, data: str):
        """
        Deserialize the string to a record.
        """
        raise NotImplementedError


T_RECORD = T.TypeVar("T_RECORD", bound=AbcRecord)


class AbcBuffer(abc.ABC):
    """
    Buffer is used to store records before they are sent via HTTP request.
    So we can fully utilize the network bandwidth.

    Buffer naturally is a FIFO queue, when you take records out of it,
    older records are taken out first.

    Buffer should be fault-tolerant. So it should be able to recover from a crash.
    For example, when you put record to buffer, it should persist the record immediately.

    Buffer should have a max number of records and max size (in Bytes).
    When the in-memory queue is full (reach any of the max), it should write
    in-memory data to a persistent storage, and clear the in-memory queue.

    User could emit records from the buffer, and then send them via HTTP request.
    User should explicitly  However,

    It should have the following attributes:

    :param max_records: Max number of records that can be stored in the buffer.
    :param max_size: Max total size of records (in bytes) that can be stored in the buffer.

    It should have the following methods:

    - :meth:`AbcBuffer.new`
    - :meth:`AbcBuffer.put`
    - :meth:`AbcBuffer.should_i_emit`
    - :meth:`AbcBuffer.emit`
    - :meth:`AbcBuffer.commit`
    """

    max_records: int
    max_bytes: int

    @classmethod
    @abc.abstractmethod
    def new(cls, **kwargs):
        """
        Factory method to create a buffer. It should try to recovery unsent records
        from persistence layer.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def put(self, record: T_RECORD):
        """
        Put a record into the in-memory queue.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def should_i_emit(self) -> bool:
        """
        Identify whether the buffer should emit records.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def emit(self) -> T.List[T_RECORD]:
        """
        Emit a list of records. Older records comes first.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def commit(self):
        """
        Mark the previously emitted records as no-longer-need.
        Typically, it removes the records from the persistence layer.
        """
        raise NotImplementedError


T_BUFFER = T.TypeVar("T_BUFFER", bound=AbcBuffer)


class AbcProducer(abc.ABC):
    buffer: T_BUFFER

    @classmethod
    @abc.abstractmethod
    def new(cls, **kwargs):
        """
        Factory method to create a producer.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def send(self, records: T.Iterable[T_RECORD]):
        """
        Send records to target. You don't need to include any logic for
        error handling, retry, buffer. Just think of how to send a batch of records.
        Those logics will be handled by the buffer and other methods.

        This is not a user oriented method. You don't need to explicitly call
        this method.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def put(
        self,
        record: T_RECORD,
        raise_send_error: bool = False,
        verbose: bool = False,
    ):
        """
        User oriented interface to produce a record. It will put the record
        to the buffer and smartly decide whether to send the records.
        """
        raise NotImplementedError


T_PRODUCER = T.TypeVar("T_PRODUCER", bound=AbcProducer)


class AbcConsumer(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def new(cls, **kwargs):
        """
        Factory method to create a consumer.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_records(self) -> T.Iterable[T_RECORD]:
        """
        Get records from the target system.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def process_record(self, record: T_RECORD):
        """
        Process a record. To indicate the processing is failed, it has to
        raise an exception.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def process_failed_record(self, record: T_RECORD):
        """
        Process a failed record.
        """
        raise NotImplementedError


T_CONSUMER = T.TypeVar("T_CONSUMER", bound=AbcConsumer)
