# Source: https://docs.delta.io/latest/delta-utility.html

Table utility commands

Delta tables support a number of utility commands.

For many Delta Lake operations, you enable integration with Apache Spark DataSourceV2 and Catalog APIs (since 3.0) by setting configurations when you create a new
SparkSession
. See
Configure SparkSession
.

Remove files no longer referenced by a Delta table
Section titled “Remove files no longer referenced by a Delta table”

You can remove files no longer referenced by a Delta table and are older than the retention threshold by running the
vacuum
 command on the table.
vacuum
 is not triggered automatically. The default retention threshold for the files is 7 days. To change this behavior, see
Data retention
.

  SQL

  Python

  Scala

  Java

VACUUM eventsTable
-- This runs VACUUM in ‘FULL’ mode and deletes data files outside of the retention duration and all files in the table directory not referenced by the table.

VACUUM eventsTable LITE
-- This VACUUM in ‘LITE’ mode runs faster.

-- Instead of finding all files in the table directory, `VACUUM LITE` uses the Delta transaction log to identify and remove files no longer referenced by any table versions within the retention duration.

-- If `VACUUM LITE` cannot be completed because the Delta log has been pruned a `DELTA_CANNOT_VACUUM_LITE` exception is raised.

-- This mode is available only in Delta 3.3 and above.

VACUUM
'
/data/events
'

-- vacuum files in path-based table

VACUUM delta.
`
/data/events/
`

VACUUM delta.
`
/data/events/
`
 RETAIN
100

HOURS

-- vacuum files not required by versions more than 100 hours old

VACUUM eventsTable DRY RUN
-- do dry run to get the list of files to be deleted

VACUUM eventsTable
USING
 INVENTORY inventoryTable  —
-
 vacuum files based
on
 a provided reservoir of files
as
 a delta
table

VACUUM eventsTable
USING
 INVENTORY (
select

*

from
 inventoryTable)  —
-
 vacuum files based
on
 a provided reservoir of files
as
 spark
SQL
 query

from
 delta.tables
import

*

deltaTable
=
 DeltaTable.
forPath
(
spark
,
 pathToTable
)
# path-based tables, or
deltaTable
=
 DeltaTable.
forName
(
spark
,
 tableName
)
# Hive metastore-based tables

deltaTable.
vacuum
()
# vacuum files not required by versions older than the default retention period

deltaTable.
vacuum
(
100
)
# vacuum files not required by versions more than 100 hours old

import
 io.delta.tables._

val

deltaTable

=

DeltaTable
.forPath(spark, pathToTable)

deltaTable.vacuum()
// vacuum files not required by versions older than the default retention period

deltaTable.vacuum(
100
)
// vacuum files not required by versions more than 100 hours old

import

io.delta.tables.
*
;
import

org.apache.spark.sql.functions
;

DeltaTable

deltaTable

=

DeltaTable
.
forPath
(
spark, pathToTable
)
;

deltaTable
.
vacuum
()
;
// vacuum files not required by versions older than the default retention period

deltaTable
.
vacuum
(
100
)
;
// vacuum files not required by versions more than 100 hours old

See the
Delta Lake APIs
 for Scala, Java, and Python syntax details.

Inventory Table
Section titled “Inventory Table”

An inventory table contains a list of file paths together with their size, type (directory or not), and the last modification time. When an INVENTORY option is provided, VACUUM will consider the files listed there instead of doing the full listing of the table directory, which can be time consuming for very large tables. The inventory table can be specified as a delta table or a spark SQL query that gives the expected table schema. The schema should be as follows:

Column Name
Type
Description
path
string
fully qualified uri
length
integer
size in bytes
isDir
boolean
boolean indicating if it is a directory
modificationTime
integer
file update time in milliseconds

Retrieve Delta table history
Section titled “Retrieve Delta table history”

You can retrieve information on the operations, user, timestamp, and so on for each write to a Delta table by running the
history
 command. The operations are returned in reverse chronological order. By default table history is retained for 30 days.

See
Configure SparkSession
 for the steps to enable support for SQL commands in Apache Spark.

  SQL

  Python

  Scala

  Java

DESCRIBE HISTORY
'
/data/events/
'

-- get the full history of the table

DESCRIBE HISTORY delta.
`
/data/events/
`

DESCRIBE HISTORY
'
/data/events/
'

LIMIT

1

-- get the last operation only

DESCRIBE HISTORY eventsTable

from
 delta.tables
import

*

deltaTable
=
 DeltaTable.
forPath
(
spark
,
 pathToTable
)

fullHistoryDF
=
 deltaTable.
history
()
# get the full history of the table

lastOperationDF
=
 deltaTable.
history
(
1
)
# get the last operation

import
 io.delta.tables._

val

deltaTable

=

DeltaTable
.forPath(spark, pathToTable)

val

fullHistoryDF

=
 deltaTable.history()
// get the full history of the table

val

lastOperationDF

=
 deltaTable.history(
1
)
// get the last operation

import

io.delta.tables.
*
;

DeltaTable

deltaTable

=

DeltaTable
.
forPath
(
spark, pathToTable
)
;

DataFrame

fullHistoryDF

=

deltaTable
.
history
()
;
// get the full history of the table

DataFrame

lastOperationDF

=

deltaTable
.
history
(
1
)
;
// fetch the last operation on the DeltaTable

See the
Delta Lake APIs
 for Scala/Java/Python syntax details.

The output of the
history
 operation has the following columns.

Column
Type
Description
version
long
Table version generated by the operation.
timestamp
timestamp
When this version was committed.
userId
string
ID of the user that ran the operation.
userName
string
Name of the user that ran the operation.
operation
string
Name of the operation.
operationParameters
map
Parameters of the operation (for example, predicates.)
job
struct
Details of the job that ran the operation.
notebook
struct
Details of notebook from which the operation was run.
clusterId
string
ID of the cluster on which the operation ran.
readVersion
long
Version of the table that was read to perform the write operation.
isolationLevel
string
Isolation level used for this operation.
isBlindAppend
boolean
Whether this operation appended data.
operationMetrics
map
Metrics of the operation (for example, number of rows and files modified.)
userMetadata
string
User-defined commit metadata if it was specified

+-------+-------------------+------+--------+---------+--------------------+----+--------+---------+-----------+--------------+-------------+--------------------+
|version|          timestamp|userId|userName|operation| operationParameters| job|notebook|clusterId|readVersion|isolationLevel|isBlindAppend|    operationMetrics|
+-------+-------------------+------+--------+---------+--------------------+----+--------+---------+-----------+--------------+-------------+--------------------+
|      5|2019-07-29 14:07:47|  null|    null|   DELETE|[predicate -> ["(...|null|    null|     null|          4|  Serializable|        false|[numTotalRows -> ...|
|      4|2019-07-29 14:07:41|  null|    null|   UPDATE|[predicate -> (id...|null|    null|     null|          3|  Serializable|        false|[numTotalRows -> ...|
|      3|2019-07-29 14:07:29|  null|    null|   DELETE|[predicate -> ["(...|null|    null|     null|          2|  Serializable|        false|[numTotalRows -> ...|
|      2|2019-07-29 14:06:56|  null|    null|   UPDATE|[predicate -> (id...|null|    null|     null|          1|  Serializable|        false|[numTotalRows -> ...|
|      1|2019-07-29 14:04:31|  null|    null|   DELETE|[predicate -> ["(...|null|    null|     null|          0|  Serializable|        false|[numTotalRows -> ...|
|      0|2019-07-29 14:01:40|  null|    null|    WRITE|[mode -> ErrorIfE...|null|    null|     null|       null|  Serializable|         true|[numFiles -> 2, n...|
+-------+-------------------+------+--------+---------+--------------------+----+--------+---------+-----------+--------------+-------------+--------------------+

The
history
 operation returns a collection of operations metrics in the
operationMetrics
 column map.

The following table lists the map key definitions by operation.

Operation
Metric name
Description
WRITE, CREATE TABLE AS SELECT, REPLACE TABLE AS SELECT, COPY INTO
numFiles
Number of files written.
numOutputBytes
Size in bytes of the written contents.
numOutputRows
Number of rows written.
STREAMING UPDATE
numAddedFiles
Number of files added.
numRemovedFiles
Number of files removed.
numOutputRows
Number of rows written.
numOutputBytes
Size of write in bytes.
DELETE
numAddedFiles
Number of files added. Not provided when partitions of the table are deleted.
numRemovedFiles
Number of files removed.
numDeletedRows
Number of rows removed. Not provided when partitions of the table are deleted.
numCopiedRows
Number of rows copied in the process of deleting files.
executionTimeMs
Time taken to execute the entire operation.
scanTimeMs
Time taken to scan the files for matches.
rewriteTimeMs
Time taken to rewrite the matched files.
TRUNCATE
numRemovedFiles
Number of files removed.
executionTimeMs
Time taken to execute the entire operation.
MERGE
numSourceRows
Number of rows in the source DataFrame.
numTargetRowsInserted
Number of rows inserted into the target table.
numTargetRowsUpdated
Number of rows updated in the target table.
numTargetRowsDeleted
Number of rows deleted in the target table.
numTargetRowsCopied
Number of target rows copied.
numOutputRows
Total number of rows written out.
numTargetFilesAdded
Number of files added to the sink(target).
numTargetFilesRemoved
Number of files removed from the sink(target).
executionTimeMs
Time taken to execute the entire operation.
scanTimeMs
Time taken to scan the files for matches.
rewriteTimeMs
Time taken to rewrite the matched files.
UPDATE
numAddedFiles
Number of files added.
numRemovedFiles
Number of files removed.
numUpdatedRows
Number of rows updated.
numCopiedRows
Number of rows just copied over in the process of updating files.
executionTimeMs
Time taken to execute the entire operation.
scanTimeMs
Time taken to scan the files for matches.
rewriteTimeMs
Time taken to rewrite the matched files.
FSCK
numRemovedFiles
Number of files removed.
CONVERT
numConvertedFiles
Number of Parquet files that have been converted.
OPTIMIZE
numAddedFiles
Number of files added.
numRemovedFiles
Number of files optimized.
numAddedBytes
Number of bytes added after the table was optimized.
numRemovedBytes
Number of bytes removed.
minFileSize
Size of the smallest file after the table was optimized.
p25FileSize
Size of the 25th percentile file after the table was optimized.
p50FileSize
Median file size after the table was optimized.
p75FileSize
Size of the 75th percentile file after the table was optimized.
maxFileSize
Size of the largest file after the table was optimized.
VACUUM
numDeletedFiles
Number of deleted files.
numVacuumedDirectories
Number of vacuumed directories.
numFilesToDelete
Number of files to delete.
RESTORE
tableSizeAfterRestore
Table size in bytes after restore.
numOfFilesAfterRestore
Number of files in the table after restore.
numRemovedFiles
Number of files removed by the restore operation.
numRestoredFiles
Number of files that were added as a result of the restore.
removedFilesSize
Size in bytes of files removed by the restore.
restoredFilesSize
Size in bytes of files added by the restore.

Show Delta table partitions
Section titled “Show Delta table partitions”

You can list the partitions of a partitioned Delta table using
SHOW PARTITIONS
.

Unlike Spark’s native
SHOW PARTITIONS
, Delta returns one typed column for each partition key instead of a single
key=value/...
 string. You can also provide an optional
PARTITION (...)
 clause to filter the returned partitions.

See
Configure SparkSession
 for steps to enable support for SQL commands in Apache Spark.

  SQL

SHOW PARTITIONS eventsTable;
+----------+-------+
| date     | region|
+----------+-------+
|2024-01-01|us     |
|2024-01-02|eu     |
+----------+-------+
SHOW PARTITIONS eventsTable
PARTITION
 (
date

=

'
2024-01-01
'
);
+----------+------+
| date     |region|
+----------+------+
|2024-01-01|us    |
+----------+------+
SHOW PARTITIONS delta.
`
/data/events/
`
;
+----------+-------+
| date     | region|
+----------+-------+
|2024-01-01|us     |
|2024-01-02|eu     |
+----------+-------+

Retrieve Delta table details
Section titled “Retrieve Delta table details”

You can retrieve detailed information about a Delta table (for example, number of files, data size) using
DESCRIBE DETAIL
.

See
Configure SparkSession
 for the steps to enable support for SQL commands in Apache Spark.

  SQL

  Python

  Scala

  Java

DESCRIBE DETAIL
'
/data/events/
'

DESCRIBE DETAIL eventsTable

from
 delta.tables
import

*

deltaTable
=
 DeltaTable.
forPath
(
spark
,
 pathToTable
)

detailDF
=
 deltaTable.
detail
()

import
 io.delta.tables._

val

deltaTable

=

DeltaTable
.forPath(spark, pathToTable)

val

detailDF

=
 deltaTable.detail()

import

io.delta.tables.
*
;

DeltaTable

deltaTable

=

DeltaTable
.
forPath
(
spark, pathToTable
)
;

DataFrame

detailDF

=

deltaTable
.
detail
()
;

See the
Delta Lake APIs
 for Scala/Java/Python syntax details.

The output of this operation has only one row with the following schema.

Column
Type
Description
format
string
Format of the table, that is,
delta
.
id
string
Unique ID of the table.
name
string
Name of the table as defined in the metastore.
description
string
Description of the table.
location
string
Location of the table.
createdAt
timestamp
When the table was created.
lastModified
timestamp
When the table was last modified.
partitionColumns
array of strings
Names of the partition columns if the table is partitioned.
numFiles
long
Number of the files in the latest version of the table.
sizeInBytes
int
The size of the latest snapshot of the table in bytes.
properties
string-string map
All the properties set for this table.
minReaderVersion
int
Minimum version of readers (according to the log protocol) that can read the table.
minWriterVersion
int
Minimum version of writers (according to the log protocol) that can write to the table.

+------+--------------------+------------------+-----------+--------------------+--------------------+-------------------+----------------+--------+-----------+----------+----------------+----------------+
|format|                  id|              name|description|            location|           createdAt|       lastModified|partitionColumns|numFiles|sizeInBytes|properties|minReaderVersion|minWriterVersion|
+------+--------------------+------------------+-----------+--------------------+--------------------+-------------------+----------------+--------+-----------+----------+----------------+----------------+
| delta|d31f82d2-a69f-42e...|default.deltatable|       null|file:/Users/tuor/...|2020-06-05 12:20:...|2020-06-05 12:20:20|              []|      10|      12345|        []|               1|               2|
+------+--------------------+------------------+-----------+--------------------+--------------------+-------------------+----------------+--------+-----------+----------+----------------+----------------+

Generate a manifest file
Section titled “Generate a manifest file”

You can a generate manifest file for a Delta table that can be used by other processing engines (that is, other than Apache Spark) to read the Delta table. For example, to generate a manifest file that can be used by Presto and Athena to read a Delta table, you run the following:

  SQL

  Python

  Scala

  Java

GENERATE symlink_format_manifest
FOR

TABLE
 delta.
`
<path-to-delta-table>
`

deltaTable
=
 DeltaTable.
forPath
(
<
path
-
to
-
delta
-
table
>
)
deltaTable.
generate
(
"
symlink_format_manifest
"
)

val

deltaTable

=

DeltaTable
.forPath(
<
path-to-delta-table
>
)
deltaTable.generate(
"
symlink_format_manifest
"
)

DeltaTable

deltaTable

=

DeltaTable
.
forPath
(
<
path
-
to
-
delta
-
table
>
)
;
deltaTable
.
generate
(
"
symlink_format_manifest
"
)
;

See
Configure SparkSession
 for the steps to enable support for SQL commands in Apache Spark.

Convert a Parquet table to a Delta table
Section titled “Convert a Parquet table to a Delta table”

Convert a Parquet table to a Delta table in-place. This command lists all the files in the directory, creates a Delta Lake transaction log that tracks these files, and automatically infers the data schema by reading the footers of all Parquet files. If your data is partitioned, you must specify the schema of the partition columns as a DDL-formatted string (that is,
<column-name1> <type>, <column-name2> <type>, ...
).

By default, this command will collect per-file statistics (e.g. minimum and maximum values for each column). These statistics will be used at query time to provide faster queries. You can disable this statistics collection in the SQL API using
NO STATISTICS
.

  SQL

  Python

  Scala

  Java

-- Convert unpartitioned Parquet table at path '<path-to-table>'
CONVERT
TO
 DELTA
parquet
.
`
<path-to-table>
`

-- Convert unpartitioned Parquet table and disable statistics collection
CONVERT
TO
 DELTA
parquet
.
`
<path-to-table>
`

NO

STATISTICS

-- Convert partitioned Parquet table at path '<path-to-table>' and partitioned by integer columns named 'part' and 'part2'
CONVERT
TO
 DELTA
parquet
.
`
<path-to-table>
`
 PARTITIONED
BY
 (part
int
, part2
int
)

-- Convert partitioned Parquet table and disable statistics collection
CONVERT
TO
 DELTA
parquet
.
`
<path-to-table>
`

NO

STATISTICS
 PARTITIONED
BY
 (part
int
, part2
int
)

from
 delta.tables
import

*

# Convert unpartitioned Parquet table at path '<path-to-table>'
deltaTable
=
 DeltaTable.
convertToDelta
(
spark
,

"
parquet.`<path-to-table>`
"
)

# Convert partitioned parquet table at path '<path-to-table>' and partitioned by integer column named 'part'
partitionedDeltaTable
=
 DeltaTable.
convertToDelta
(
spark
,

"
parquet.`<path-to-table>`
"
,

"
part int
"
)

import
 io.delta.tables._

// Convert unpartitioned Parquet table at path '<path-to-table>'
val

deltaTable

=

DeltaTable
.convertToDelta(spark,
"
parquet.`<path-to-table>`
"
)

// Convert partitioned Parquet table at path '<path-to-table>' and partitioned by integer columns named 'part' and 'part2'
val

partitionedDeltaTable

=

DeltaTable
.convertToDelta(spark,
"
parquet.`<path-to-table>`
"
,
"
part int, part2 int
"
)

import

io.delta.tables.
*
;

// Convert unpartitioned Parquet table at path '<path-to-table>'
DeltaTable

deltaTable

=

DeltaTable
.
convertToDelta
(
spark,
"
parquet.`<path-to-table>`
"
)
;

// Convert partitioned Parquet table at path '<path-to-table>' and partitioned by integer columns named 'part' and 'part2'
DeltaTable

deltaTable

=

DeltaTable
.
convertToDelta
(
spark,
"
parquet.`<path-to-table>`
"
,
"
part int, part2 int
"
)
;

Convert an Iceberg table to a Delta table
Section titled “Convert an Iceberg table to a Delta table”

You can convert an Iceberg table to a Delta table in place if the underlying file format of the Iceberg table is Parquet. Similar to a conversion from a Parquet table, the conversion is in-place and there won’t be any data copy or data rewrite. The original Iceberg table and the converted Delta table have separate history, so modifying the Delta table should not affect the Iceberg table as long as the source data Parquet files are not touched or deleted.

The following command creates a Delta Lake transaction log based on the Iceberg table’s native file manifest, schema and partitioning information. The converter also collects column stats during the conversion, unless
NO STATISTICS
 is specified.

  SQL

-- Convert the Iceberg table in the path <path-to-table>.
CONVERT
TO
 DELTA iceberg.\
`
<path-to-table>
\`

-- Convert the Iceberg table in the path <path-to-table> without collecting statistics.
CONVERT TO DELTA iceberg.
\`
<path-to-table>
\`
 NO STATISTICS

Convert a Delta table to a Parquet table
Section titled “Convert a Delta table to a Parquet table”

You can easily convert a Delta table back to a Parquet table using the following steps:

If you have performed Delta Lake operations that can change the data files (for example,
delete
 or
merge
), run
vacuum
 ) with retention of 0 hours to delete all data files that do not belong to the latest version of the table.

Delete the
_delta_log
 directory in the table directory.

Restore a Delta table to an earlier state
Section titled “Restore a Delta table to an earlier state”

You can restore a Delta table to its earlier state by using the
RESTORE
 command. A Delta table internally maintains historic versions of the table that enable it to be restored to an earlier state. A version corresponding to the earlier state or a timestamp of when the earlier state was created are supported as options by the
RESTORE
 command.

  SQL

  Python

  Scala

  Java

RESTORE

TABLE

db
.
target_table

TO

VERSION

AS
 OF
<version>
RESTORE

TABLE
 delta.
`
/data/target/
`

TO

TIMESTAMP

AS
 OF
<timestamp>

from
 delta.tables
import

*

deltaTable
=
 DeltaTable.
forPath
(
spark
,

<
path
-
to
-
table
>
)
# path-based tables, or
deltaTable
=
 DeltaTable.
forName
(
spark
,

<
table
-
name
>
)
# Hive metastore-based tables

deltaTable.
restoreToVersion
(
0
)
# restore table to oldest version

deltaTable.
restoreToTimestamp
(
'
2019-02-14
'
)
# restore to a specific timestamp

import
 io.delta.tables._

val

deltaTable

=

DeltaTable
.forPath(spark,
<
path-to-table
>
)
val

deltaTable

=

DeltaTable
.forName(spark,
<
table-name
>
)

deltaTable.restoreToVersion(
0
)
// restore table to oldest version

deltaTable.restoreToTimestamp(
"
2019-02-14
"
)
// restore to a specific timestamp

import

io.delta.tables.
*
;

DeltaTable

deltaTable

=

DeltaTable
.
forPath
(
spark,
<
path
-
to
-
table
>
)
;
DeltaTable

deltaTable

=

DeltaTable
.
forName
(
spark,
<
table
-
name
>
)
;

deltaTable
.
restoreToVersion
(
0
)

// restore table to oldest version

deltaTable
.
restoreToTimestamp
(
"
2019-02-14
"
)

// restore to a specific timestamp

For example:

Table version
Operation
Delta log updates
Records in data change log updates
0
INSERT
AddFile(/path/to/file-1, dataChange = true)
(name = Viktor, age = 29), (name = George, age = 55)
1
INSERT
AddFile(/path/to/file-2, dataChange = true)
(name = George, age = 39)
2
OPTIMIZE
AddFile(/path/to/file-3, dataChange = false), RemoveFile(/path/to/file-1), RemoveFile(/path/to/file-2)
(No records as Optimize compaction does not change the data in the table)
3
RESTORE(version=1)
RemoveFile(/path/to/file-3), AddFile(/path/to/file-1, dataChange = true), AddFile(/path/to/file-2, dataChange = true)
(name = Viktor, age = 29), (name = George, age = 55), (name = George, age = 39)

In the preceding example, the
RESTORE
 command results in updates that were already seen when reading the Delta table version 0 and 1. If a streaming query was reading this table, then these files will be considered as newly added data and will be processed again.

RESTORE
 reports the following metrics as a single row DataFrame once the operation is complete:

table_size_after_restore
: The size of the table after restoring.

num_of_files_after_restore
: The number of files in the table after restoring.

num_removed_files
: Number of files removed (logically deleted) from the table.

num_restored_files
: Number of files restored due to rolling back.

removed_files_size
: Total size in bytes of the files that are removed from the table.

restored_files_size
: Total size in bytes of the files that are restored.

Shallow clone a Delta table
Section titled “Shallow clone a Delta table”

You can create a shallow copy of an existing Delta table at a specific version using the
shallow clone
 command.

Any changes made to shallow clones affect only the clones themselves and not the source table, as long as they don’t touch the source data Parquet files.

The metadata that is cloned includes: schema, partitioning information, invariants, nullability. For shallow clones, stream metadata is not cloned. Metadata not cloned are the table description and
user-defined commit metadata
.

  SQL

CREATE

TABLE

delta
.
`
/data/target/
`
 SHALLOW CLONE delta.
`
/data/source/
`

-- Create a shallow clone of /data/source at /data/target

CREATE OR REPLACE

TABLE

db
.target_table SHALLOW CLONE
db
.
source_table

-- Replace the target. target needs to be emptied

CREATE

TABLE

IF

NOT

EXISTS
 delta.
`
/data/target/
`
 SHALLOW CLONE
db
.
source_table

-- No-op if the target table exists

CREATE

TABLE

db
.target_table SHALLOW CLONE delta.
`
/data/source
`

CREATE

TABLE

db
.target_table SHALLOW CLONE delta.
`
/data/source
`

VERSION

AS
 OF
version

CREATE

TABLE

db
.target_table SHALLOW CLONE delta.
`
/data/source
`

TIMESTAMP

AS
 OF timestamp_expression
-- timestamp can be like “2019-01-01” or like date_sub(current_date(), 1)

CLONE
 reports the following metrics as a single row DataFrame once the operation is complete:

source_table_size
: Size of the source table that’s being cloned in bytes.

source_num_of_files
: The number of files in the source table.

Cloud provider permissions
Section titled “Cloud provider permissions”

If you have created a shallow clone, any user that reads the shallow clone needs permission to read the files in the original table, since the data files remain in the source table’s directory where we cloned from. To make changes to the clone, users will need write access to the clone’s directory.

Clone use cases
Section titled “Clone use cases”

Machine learning flow reproduction
Section titled “Machine learning flow reproduction”

When doing machine learning, you may want to archive a certain version of a table on which you trained an ML model. Future models can be tested using this archived data set.

  SQL

-- Trained model on version 15 of Delta table
CREATE

TABLE

delta
.
`
/model/dataset
`
 SHALLOW CLONE entire_dataset
VERSION

AS
 OF
15

Short-term experiments on a production table
Section titled “Short-term experiments on a production table”

To test a workflow on a production table without corrupting the table, you can easily create a shallow clone. This allows you to run arbitrary workflows on the cloned table that contains all the production data but does not affect any production workloads.

  SQL

-- Perform shallow clone
CREATE OR REPLACE

TABLE

my_test
 SHALLOW CLONE my_prod_table;

UPDATE
 my_test
WHERE
 user_id
is

null

SET
 invalid
=
true;
-- Run a bunch of validations. Once happy:

-- This should leverage the update information in the clone to prune to only
-- changed files in the clone if possible
MERGE

INTO
 my_prod_table
USING
 my_test
ON

my_test
.
user_id

<=>

my_prod_table
.
user_id
WHEN

MATCHED

AND

my_test
.
user_id

is

null

THEN

UPDATE

*
;

DROP

TABLE
 my_test;

Table property overrides
Section titled “Table property overrides”

Table property overrides are particularly useful for:

Annotating tables with owner or user information when sharing data with different business units.

Archiving Delta tables and time travel is required. You can specify the log retention period independently for the archive table. For example:

  SQL

CREATE OR REPLACE

TABLE

archive
.my_table SHALLOW CLONE
prod
.
my_table
TBLPROPERTIES (

delta
.
logRetentionDuration

=

'
3650 days
'
,

delta
.
deletedFileRetentionDuration

=

'
3650 days
'
)
LOCATION

'
xx://archive/my_table
'

Clone Parquet or Iceberg table to Delta
Section titled “Clone Parquet or Iceberg table to Delta”

Shallow clone for Parquet and Iceberg combines functionality used to clone Delta tables and convert tables to Delta Lake, you can use clone functionality to convert data from Parquet or Iceberg data sources to managed or external Delta tables with the same basic syntax.

replace
 has the same limitation as Delta shallow clone, the target table must be emptied before applying replace.

  SQL

CREATE

OR

REPLACE

TABLE

<
target_table_name
>
 SHALLOW CLONE
parquet
.
`
/path/to/data
`
;

CREATE

OR

REPLACE

TABLE

<
target_table_name
>
 SHALLOW CLONE iceberg.
`
/path/to/data
`
;
