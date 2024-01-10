.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add ``KafkaProducer``.
- Add ``DynamoDBCheckpoint``.
- Add ``AwsKinesisStreamConsumer``.

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.3.1 (2024-01-09)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Re-design the code base. Put concrete class and base class in different modules.
- Add the abstract :class:`~abstract_producer.consumer.CheckPoint` base class.
- Rename ``AwsKinesisConsumer`` to ``PocAwsKinesisConsumer`` because it uses local file for checkpoint, which is not ideal for production.
- Add retry exponential backoff to all ``Consumer``.
- Add the following public API:
    - ``abstract_producer.api.SimpleCheckpoint``
    - ``abstract_producer.api.SimpleConsumer``
    - ``abstract_producer.api.PocAwsKinesisStreamConsumer``

**Minor Improvements**

- greatly improve the document
- greatly improve the unit test
- greatly improve the examples


0.2.1 (2024-01-05)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add concrete implementations ``KinesisRecord``, ``KinesisGetRecordsResponseRecord``, ``AwsKinesisStreamProducer``, ``AwsKinesisConsumer``.

- Add the following public API:
    - ``abstract_producer.api.KinesisRecord``
    - ``abstract_producer.api.T_KINESIS_RECORD``
    - ``abstract_producer.api.KinesisGetRecordsResponseRecord``
    - ``abstract_producer.api.T_KINESIS_GET_RECORDS_RESPONSE_RECORD``
    - ``abstract_producer.api.AwsKinesisStreamProducer``
    - ``abstract_producer.api.Shard``
    - ``abstract_producer.api.AwsKinesisConsumer``


0.1.1 (2024-01-03)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- First release
- Add the base class ``BaseRecord``, ``BaseBuffer``, ``BaseProducer``.
- Add concrete implementations ``DataClassRecord``, ``FileBuffer``, ``SimpleProducer``, ``AwsCloudWatchLogsProducer``.
- Add the following public API:
    - ``abstract_producer.api.T_RECORD``
    - ``abstract_producer.api.T_BUFFER``
    - ``abstract_producer.api.T_PRODUCER``
    - ``abstract_producer.api.BaseRecord``
    - ``abstract_producer.api.DataClassRecord``
    - ``abstract_producer.api.BaseBuffer``
    - ``abstract_producer.api.FileBuffer``
    - ``abstract_producer.api.BaseProducer``
    - ``abstract_producer.api.SimpleProducer``
    - ``abstract_producer.api.exc``
    - ``abstract_producer.api.utils``
    - ``abstract_producer.api.AwsCloudWatchLogsProducer``
