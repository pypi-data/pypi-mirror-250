# -*- coding: utf-8 -*-

"""
Usage example::

    >>> import abstract_producer.api as abstract_producer

    >>> abstract_producer.DataClassRecord
    >>> abstract_producer.FileBuffer
    >>> abstract_producer.SimpleProducer
"""

from .logger import logger
from .abstraction import T_RECORD
from .abstraction import T_BUFFER
from .abstraction import T_PRODUCER
from .record import BaseRecord
from .buffer import BaseBuffer
from .producer import RetryConfig
from .producer import BaseProducer
from .consumer import StatusEnum
from .consumer import Tracker
from .consumer import T_POINTER
from .consumer import CheckPoint
from .consumer import T_CHECK_POINT
from .consumer import BaseConsumer
from . import exc
from . import utils
from .records.dataclass import DataClassRecord
from .records.dataclass import T_DATA_CLASS_RECORD
from .buffers.file_buffer import FileBuffer
from .producers.simple import SimpleProducer
from .consumers.simple import SimpleCheckpoint
from .consumers.simple import SimpleConsumer

try:
    from .records.aws_kinesis import KinesisRecord
    from .records.aws_kinesis import T_KINESIS_RECORD
    from .records.aws_kinesis import KinesisGetRecordsResponseRecord
    from .records.aws_kinesis import T_KINESIS_GET_RECORDS_RESPONSE_RECORD
except ImportError:  # pragma: no cover
    pass

try:
    from .producers.aws_cloudwatch_logs import AwsCloudWatchLogsProducer
    from .producers.aws_kinesis import AwsKinesisStreamProducer
except ImportError:  # pragma: no cover
    pass

try:
    from .consumers.aws_kinesis import Shard
    from .consumers.aws_kinesis import PocAwsKinesisStreamConsumer
except ImportError:  # pragma: no cover
    pass
