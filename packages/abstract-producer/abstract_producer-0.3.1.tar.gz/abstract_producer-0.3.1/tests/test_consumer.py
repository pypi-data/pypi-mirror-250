# -*- coding: utf-8 -*-

from abstract_producer.consumer import (
    StatusEnum,
    Tracker,
    T_POINTER,
    CheckPoint,
    T_CHECK_POINT,
    BaseConsumer,
)


class TestCheckPoint:
    def test(self):
        pass


class TestBaseConsumer:
    def test(self):
        pass


if __name__ == "__main__":
    from abstract_producer.tests import run_cov_test

    run_cov_test(__file__, "abstract_producer.consumer", preview=False)
