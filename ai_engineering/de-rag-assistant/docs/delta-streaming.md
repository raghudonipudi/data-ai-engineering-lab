# Source: https://docs.delta.io/latest/delta-streaming.html

Table streaming reads and writes

Delta Lake is deeply integrated with
Spark Structured Streaming
 through
readStream
 and
writeStream
. Delta Lake overcomes many of the limitations typically associated with streaming systems and files, including:

Maintaining “exactly-once” processing with more than one stream (or concurrent batch jobs)

Efficiently discovering which files are new when using files as the source for a stream

For many Delta Lake operations on tables, you enable integration with Apache Spark DataSourceV2 and Catalog APIs (since 3.0) by setting configurations when you create a new
SparkSession
. See
Configure SparkSession
.

Delta table as a source
Section titled “Delta table as a source”

When you load a Delta table as a stream source and use it in a streaming query, the query processes all of the data present in the table as well as any new data that arrives after the stream is started.

  Scala

spark.readStream.format(
"
delta
"
)

.load(
"
/tmp/delta/events
"
)

import
 io.delta.implicits._
spark.readStream.delta(
"
/tmp/delta/events
"
)

Limit input rate
Section titled “Limit input rate”

The following options are available to control micro-batches:

maxFilesPerTrigger
: How many new files to be considered in every micro-batch. The default is 1000.

maxBytesPerTrigger
: How much data gets processed in each micro-batch. This option sets a “soft max”, meaning that a batch processes approximately this amount of data and may process more than the limit in order to make the streaming query move forward in cases when the smallest input unit is larger than this limit. If you use
Trigger.Once
 for your streaming, this option is ignored. This is not set by default.

If you use
maxBytesPerTrigger
 in conjunction with
maxFilesPerTrigger
, the micro-batch processes data until either the
maxFilesPerTrigger
 or
maxBytesPerTrigger
 limit is reached.

Ignore updates and deletes
Section titled “Ignore updates and deletes”

Structured Streaming does not handle input that is not an append and throws an exception if any modifications occur on the table being used as a source. There are two main strategies for dealing with changes that cannot be automatically propagated downstream:

You can delete the output and checkpoint and restart the stream from the beginning.

You can set one of the following options:

skipChangeCommits
 (recommended): skip commits that contain data-changing operations such as
UPDATE
,
MERGE INTO
,
DELETE
, or
OVERWRITE
. Skipped commits are not processed, so downstream does not see rows from those commits.

ignoreDeletes
 (legacy): ignore transactions that delete data at partition boundaries.

ignoreChanges
 (deprecated in favor of
skipChangeCommits
): re-process updates if files had to be rewritten in the source table due to a data changing operation such as
UPDATE
,
MERGE INTO
,
DELETE
 (within partitions), or
OVERWRITE
. Unchanged rows may still be emitted, therefore your downstream consumers should be able to handle duplicates. Deletes are not propagated downstream.
ignoreChanges
 subsumes
ignoreDeletes
. Therefore if you use
ignoreChanges
, your stream will not be disrupted by either deletions or updates to the source table.

Specify initial position
Section titled “Specify initial position”

You can use the following options to specify the starting point of the Delta Lake streaming source without processing the entire table.

startingVersion
: The Delta Lake version to start from. All table changes starting from this version (inclusive) will be read by the streaming source. You can obtain the commit versions from the
version
 column of the
DESCRIBE HISTORY
 command output.

To return only the latest changes, specify
latest
.

startingTimestamp
: The timestamp to start from. All table changes committed at or after the timestamp (inclusive) will be read by the streaming source. One of:

A timestamp string. For example,
"2019-01-01T00:00:00.000Z"
.

A date string. For example,
"2019-01-01"
.

You cannot set both options at the same time; you can use only one of them. They take effect only when starting a new streaming query. If a streaming query has started and the progress has been recorded in its checkpoint, these options are ignored.

Example
Section titled “Example”

For example, suppose you have a table
user_events
. If you want to read changes since version 5, use:

  Scala

spark.readStream.format(
"
delta
"
)

.option(
"
startingVersion
"
,
"
5
"
)

.load(
"
/tmp/delta/user_events
"
)

If you want to read changes since 2018-10-18, use:

  Scala

spark.readStream.format(
"
delta
"
)

.option(
"
startingTimestamp
"
,
"
2018-10-18
"
)

.load(
"
/tmp/delta/user_events
"
)

Process initial snapshot without data being dropped
Section titled “Process initial snapshot without data being dropped”

When using a Delta table as a stream source, the query first processes all of the data present in the table. The Delta table at this version is called the initial snapshot. By default, the Delta table’s data files are processed based on which file was last modified. However, the last modification time does not necessarily represent the record event time order.

In a stateful streaming query with a defined watermark, processing files by modification time can result in records being processed in the wrong order. This could lead to records dropping as late events by the watermark.

You can avoid the data drop issue by enabling the following option:

withEventTimeOrder: Whether the initial snapshot should be processed with event time order.

With event time order enabled, the event time range of initial snapshot data is divided into time buckets. Each micro batch processes a bucket by filtering data within the time range. The maxFilesPerTrigger and maxBytesPerTrigger configuration options are still applicable to control the microbatch size but only in an approximate way due to the nature of the processing.

The graphic below shows this process:

Notable information about this feature:

The data drop issue only happens when the initial Delta snapshot of a stateful streaming query is processed in the default order.

You cannot change
withEventTimeOrder
 once the stream query is started while the initial snapshot is still being processed. To restart with
withEventTimeOrder
 changed, you need to delete the checkpoint.

If you are running a stream query with withEventTimeOrder enabled, you cannot downgrade it to a Delta version which doesn’t support this feature until the initial snapshot processing is completed. If you need to downgrade, you can wait for the initial snapshot to finish, or delete the checkpoint and restart the query.

This feature is not supported in the following uncommon scenarios:

The event time column is a generated column and there are non-projection transformations between the Delta source and watermark.

There is a watermark that has more than one Delta source in the stream query.

With event time order enabled, the performance of the Delta initial snapshot processing might be slower.

Each micro batch scans the initial snapshot to filter data within the corresponding event time range. For faster filter action, it is advised to use a Delta source column as the event time so that data skipping can be applied (check _ for when it’s applicable). Additionally, table partitioning along the event time column can further speed the processing. You can check Spark UI to see how many delta files are scanned for a specific micro batch.

Example
Section titled “Example”

Suppose you have a table
user_events
 with an
event_time
 column. Your streaming query is an aggregation query. If you want to ensure no data drop during the initial snapshot processing, you can use:

  Scala

spark.readStream.format(
"
delta
"
)

.option(
"
withEventTimeOrder
"
,
"
true
"
)

.load(
"
/tmp/delta/user_events
"
)

.withWatermark(
"
event_time
"
,
"
10 seconds
"
)

Tracking non-additive schema changes
Section titled “Tracking non-additive schema changes”

You can provide a schema tracking location to enable streaming from Delta tables with column mapping enabled. This overcomes an issue in which non-additive schema changes could result in broken streams by allowing streams to read past table data in their exact schema as if the table is time-travelled.

Each streaming read against a data source must have its own
schemaTrackingLocation
 specified. The specified
schemaTrackingLocation
 must be contained within the directory specified for the
checkpointLocation
 of the target table for streaming write.

Example
Section titled “Example”

The option
schemaTrackingLocation
 is used to specify the path for schema tracking, as shown in the following code example:

  Python

checkpoint_path
=

"
/path/to/checkpointLocation
"

(spark.readStream

.
option
(
"
schemaTrackingLocation
"
,
 checkpoint_path
)

.
table
(
"
delta_source_table
"
)

.writeStream

.
option
(
"
checkpointLocation
"
,
 checkpoint_path
)

.
toTable
(
"
output_table
"
)
)

Delta table as a sink
Section titled “Delta table as a sink”

You can also write data into a Delta table using Structured Streaming. The transaction log enables Delta Lake to guarantee exactly-once processing, even when there are other streams or batch queries running concurrently against the table.

Append mode
Section titled “Append mode”

By default, streams run in append mode, which adds new records to the table.

You can use the path method:

  Python

  Scala

events.writeStream

.
format
(
"
delta
"
)

.
outputMode
(
"
append
"
)

.
option
(
"
checkpointLocation
"
,

"
/tmp/delta/_checkpoints/
"
)

.
start
(
"
/delta/events
"
)

events.writeStream

.format(
"
delta
"
)

.outputMode(
"
append
"
)

.option(
"
checkpointLocation
"
,
"
/tmp/delta/events/_checkpoints/
"
)

.start(
"
/tmp/delta/events
"
)

import
 io.delta.implicits._
events.writeStream

.outputMode(
"
append
"
)

.option(
"
checkpointLocation
"
,
"
/tmp/delta/events/_checkpoints/
"
)

.delta(
"
/tmp/delta/events
"
)

or the
toTable
 method (in Spark 3.1 and higher) as follows:

  Python

  Scala

events.writeStream

.
format
(
"
delta
"
)

.
outputMode
(
"
append
"
)

.
option
(
"
checkpointLocation
"
,

"
/tmp/delta/events/_checkpoints/
"
)

.
toTable
(
"
events
"
)

events.writeStream

.outputMode(
"
append
"
)

.option(
"
checkpointLocation
"
,
"
/tmp/delta/events/_checkpoints/
"
)

.toTable(
"
events
"
)

Complete mode
Section titled “Complete mode”

You can also use Structured Streaming to replace the entire table with every batch. One example use case is to compute a summary using aggregation:

  Python

  Scala

(spark.readStream

.
format
(
"
delta
"
)

.
load
(
"
/tmp/delta/events
"
)

.
groupBy
(
"
customerId
"
)

.
count
()

.writeStream

.
format
(
"
delta
"
)

.
outputMode
(
"
complete
"
)

.
option
(
"
checkpointLocation
"
,

"
/tmp/delta/eventsByCustomer/_checkpoints/
"
)

.
start
(
"
/tmp/delta/eventsByCustomer
"
)
)

spark.readStream

.format(
"
delta
"
)

.load(
"
/tmp/delta/events
"
)

.groupBy(
"
customerId
"
)

.count()

.writeStream

.format(
"
delta
"
)

.outputMode(
"
complete
"
)

.option(
"
checkpointLocation
"
,
"
/tmp/delta/eventsByCustomer/_checkpoints/
"
)

.start(
"
/tmp/delta/eventsByCustomer
"
)

The preceding example continuously updates a table that contains the aggregate number of events by customer.

For applications with more lenient latency requirements, you can save computing resources with one-time triggers. Use these to update summary aggregation tables on a given schedule, processing only new data that has arrived since the last update.

Idempotent table writes in
foreachBatch
Section titled “Idempotent table writes in foreachBatch”

The command foreachBatch allows you to specify a function that is executed on the output of every micro-batch after arbitrary transformations in the streaming query. This allows implementating a
foreachBatch
 function that can write the micro-batch output to one or more target Delta table destinations. However,
foreachBatch
 does not make those writes idempotent as those write attempts lack the information of whether the batch is being re-executed or not. For example, rerunning a failed batch could result in duplicate data writes.

To address this, Delta tables support the following
DataFrameWriter
 options to make the writes idempotent:

txnAppId
: A unique string that you can pass on each
DataFrame
 write. For example, you can use the StreamingQuery ID as
txnAppId
.

txnVersion
: A monotonically increasing number that acts as transaction version.

Delta table uses the combination of
txnAppId
 and
txnVersion
 to identify duplicate writes and ignore them.

If a batch write is interrupted with a failure, rerunning the batch uses the same application and batch ID, which would help the runtime correctly identify duplicate writes and ignore them. Application ID (
txnAppId
) can be any user-generated unique string and does not have to be related to the stream ID.

The same
DataFrameWriter
 options can be used to achieve the idempotent writes in non-Streaming job. For details
Idempotent writes
.

Example
Section titled “Example”

  Python

  Scala

app_id
=

...

# A unique string that is used as an application ID.

def

writeToDeltaLakeTableIdempotent
(
batch_df
,
batch_id
)
:

batch_df.write.
format
(
...
).
option
(
"
txnVersion
"
,
 batch_id
).
option
(
"
txnAppId
"
,
 app_id
).
save
(
...
)
# location 1

batch_df.write.
format
(
...
).
option
(
"
txnVersion
"
,
 batch_id
).
option
(
"
txnAppId
"
,
 app_id
).
save
(
...
)
# location 2

val

appId

=
 ...
// A unique string that is used as an application ID.
streamingDF.writeStream.foreachBatch { (
batchDF
:
DataFrame
,
batchId
:
Long
)
=>

batchDF.write.format(...).option(
"
txnVersion
"
, batchId).option(
"
txnAppId
"
, appId).save(...)
// location 1

batchDF.write.format(...).option(
"
txnVersion
"
, batchId).option(
"
txnAppId
"
, appId).save(...)
// location 2
}
