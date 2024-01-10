# -*- coding: utf-8 -*-

from datetime import datetime
from abstract_producer.paths import dir_unit_test
from abstract_producer.consumers.simple import (
    SimpleCheckpoint,
)


class TestSimpleCheckpoint:
    def test(self):
        # prepare to create the first checkpoint, make sure the checkpoint file does not exist
        path_checkpoint = dir_unit_test.joinpath("simple_consumer_checkpoint.json")
        path_records = dir_unit_test.joinpath("simple_consumer_records.json")
        if path_checkpoint.exists():
            path_checkpoint.unlink()
        if path_records.exists():
            path_records.unlink()

        # create the first checkpoint
        checkpoint = SimpleCheckpoint.load(
            checkpoint_file=f"{path_checkpoint}",
            records_file=f"{path_records}",
        )
        assert checkpoint.initial_pointer == 0
        assert checkpoint.start_pointer == 0
        assert checkpoint.next_pointer is None
        assert checkpoint.batch_sequence == 0
        assert checkpoint.batch == {}
        assert checkpoint.path_checkpoint.exists() is True


if __name__ == "__main__":
    from abstract_producer.tests import run_cov_test

    run_cov_test(__file__, "abstract_producer.consumers.simple", preview=False)
