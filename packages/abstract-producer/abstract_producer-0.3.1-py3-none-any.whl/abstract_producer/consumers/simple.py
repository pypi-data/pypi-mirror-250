# -*- coding: utf-8 -*-

import typing as T
import json
import dataclasses
from pathlib import Path
from itertools import islice

from ..abstraction import T_RECORD
from ..consumer import (
    T_POINTER,
    Tracker,
    CheckPoint,
    T_CHECK_POINT,
    BaseConsumer,
)


@dataclasses.dataclass
class SimpleCheckpoint(CheckPoint):
    """
    A simple checkpoint using local json file for persistence.
    """

    checkpoint_file: str = dataclasses.field()
    records_file: str = dataclasses.field()

    @property
    def path_checkpoint(self) -> Path:
        return Path(self.checkpoint_file)

    @property
    def path_records(self) -> Path:
        return Path(self.records_file)

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            checkpoint_file=data["checkpoint_file"],
            records_file=data["records_file"],
            initial_pointer=data["initial_pointer"],
            start_pointer=data["start_pointer"],
            next_pointer=data["next_pointer"],
            batch_sequence=data["batch_sequence"],
            batch={
                id: Tracker.from_dict(tracker_dct)
                for id, tracker_dct in data["batch"].items()
            },
        )

    def dump(self):
        self.path_checkpoint.write_text(json.dumps(self.to_dict(), indent=4))

    @classmethod
    def load(
        cls,
        checkpoint_file: str,
        records_file: str,
        initial_pointer: T_POINTER = 0,
        start_pointer: T_POINTER = 0,
        next_pointer: T.Optional[T_POINTER] = None,
        batch_sequence: int = 0,
        batch: T.Optional[T.Dict[str, Tracker]] = None,
    ) -> T.Optional[T_CHECK_POINT]:
        path_checkpoint = Path(checkpoint_file)
        path_records = Path(records_file)
        if path_checkpoint.exists():
            return SimpleCheckpoint.from_dict(json.loads(path_checkpoint.read_text()))
        else:
            if batch is None:
                batch = dict()
            checkpoint = SimpleCheckpoint(
                checkpoint_file=str(path_checkpoint),
                records_file=str(path_records),
                initial_pointer=initial_pointer,
                start_pointer=start_pointer,
                next_pointer=next_pointer,
                batch_sequence=batch_sequence,
                batch=batch,
            )
            checkpoint.dump()
            return checkpoint

    def dump_records(self, records: T.Iterable[T_RECORD]):
        """
        Dump the records in a batch to the persistence layer.
        """
        self.path_records.write_text(
            "\n".join([record.serialize() for record in records])
        )

    def load_records(self, record_class: T_RECORD, **kwargs) -> T.List[T_RECORD]:
        """
        Load the batch records from the persistence layer.
        """
        if self.path_records.exists():
            with self.path_records.open("r") as f:
                records = [record_class.deserialize(line) for line in f.readlines()]
            return records
        else:
            return []


@dataclasses.dataclass
class SimpleConsumer(BaseConsumer):
    """
    :param record_class:
    :param path_checkpoint:
    :param path_records:
    :param path_source:
    :param path_dlq:
    :param checkpoint:
    """

    path_source: Path = dataclasses.field()
    path_dlq: Path = dataclasses.field()

    @classmethod
    def new(
        cls,
        record_class: T.Type[T_RECORD],
        consumer_id: str,
        path_source: Path,
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
            path_source=path_source,
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
    ) -> T.Tuple[T.List[T_RECORD], T_POINTER]:
        if limit is None:
            limit = self.limit
        records = list()
        try:
            with self.path_source.open("r") as f:
                for _ in range(self.checkpoint.start_pointer):
                    next(f)
                for line in islice(f, limit):
                    record = self.record_class.deserialize(line)
                    records.append(record)
        except FileNotFoundError:
            pass
        next_pointer = self.checkpoint.start_pointer + len(records)
        return records, next_pointer
