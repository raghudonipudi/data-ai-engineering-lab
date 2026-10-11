# Source: https://docs.delta.io/latest/optimizations-oss.html

Optimizations

Optimize performance with file management
Section titled “Optimize performance with file management”

To improve query speed, Delta Lake supports the ability to optimize the layout of data in storage. There are various ways to optimize the layout.

Compaction (bin-packing)
Section titled “Compaction (bin-packing)”

Delta Lake can improve the speed of read queries from a table by coalescing small files into larger ones.

  SQL

  Python

  Scala

OPTIMIZE
'
/path/to/delta/table
'

-- Optimizes the path-based Delta Lake table

OPTIMIZE delta_table_name;

OPTIMIZE delta.
`
/path/to/delta/table
`
;

-- If you have a large amount of data and only want to optimize a subset of it, you can specify an optional partition predicate using `WHERE`:
OPTIMIZE delta_table_name
WHERE

date

>=

'
2017-01-01
'

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
# For path-based tables
# For Hive metastore-based tables: deltaTable = DeltaTable.forName(spark, tableName)

deltaTable.
optimize
().
executeCompaction
()

# If you have a large amount of data and only want to optimize a subset of it, you can specify an optional partition predicate using `where`
deltaTable.
optimize
().
where
(
"
date='2021-11-18'
"
).
executeCompaction
()

import
 io.delta.tables._

val

deltaTable

=

DeltaTable
.forPath(spark, pathToTable)
// For path-based tables
// For Hive metastore-based tables: val deltaTable = DeltaTable.forName(spark, tableName)

deltaTable.optimize().executeCompaction()

// If you have a large amount of data and only want to optimize a subset of it, you can specify an optional partition predicate using `where`
deltaTable.optimize().where(
"
date='2021-11-18'
"
).executeCompaction()

For Scala, Java, and Python API syntax details, see the
Delta Lake APIs
.

Readers of Delta tables use snapshot isolation, which means that they are not interrupted when
OPTIMIZE
 removes unnecessary files from the transaction log.
OPTIMIZE
 makes no data related changes to the table, so a read before and after an
OPTIMIZE
 has the same results. Performing
OPTIMIZE
 on a table that is a streaming source does not affect any current or future streams that treat this table as a source.
OPTIMIZE
 returns the file statistics (min, max, total, and so on) for the files removed and the files added by the operation. Optimize stats also contains the number of batches, and partitions optimized.

Auto compaction
Section titled “Auto compaction”

Auto compaction combines small files within Delta table partitions to automatically reduce small file problems. Auto compaction occurs after a write to a table has succeeded and runs synchronously on the cluster that has performed the write. Auto compaction only compacts files that haven’t been compacted previously.

You can control the output file size by setting the configuration
spark.databricks.delta.autoCompact.maxFileSize
.

Auto compaction is only triggered for partitions or tables that have at least a certain number of small files. You can optionally change the minimum number of files required to trigger auto compaction by setting
spark.databricks.delta.autoCompact.minNumFiles
.

Auto compaction can be enabled at the table or session level using the following settings:

Table property:
delta.autoOptimize.autoCompact

SparkSession setting:
spark.databricks.delta.autoCompact.enabled

These settings accept the following options:

Options
Behavior
true
Enable auto compaction. By default will use 128 MB as the target file size.
false
Turns off auto compaction. Can be set at the session level to override auto compaction for all Delta tables modified in the workload.

Data skipping
Section titled “Data skipping”

Data skipping information is collected automatically when you write data into a Delta Lake table. Delta Lake takes advantage of this information (minimum and maximum values for each column) at query time to provide faster queries. You do not need to configure data skipping; the feature is activated whenever applicable. However, its effectiveness depends on the layout of your data. For best results, apply
Z-Ordering
.

Collecting statistics on a column containing long values such as
string
 or
binary
 is an expensive operation. To avoid collecting statistics on such columns you can configure the
table property

delta.dataSkippingNumIndexedCols
. This property indicates the position index of a column in the table’s schema. All columns with a position index less than the
delta.dataSkippingNumIndexedCols
 property will have statistics collected. For the purposes of collecting statistics, each field within a nested column is considered as an individual column. To avoid collecting statistics on columns containing long values, either set the
delta.dataSkippingNumIndexedCols
 property so that the long value columns are after this index in the table’s schema, or move columns containing long strings to an index position greater than the
delta.dataSkippingNumIndexedCols
 property by using
ALTER TABLE ALTER COLUMN
.

Z-Ordering (multi-dimensional clustering)
Section titled “Z-Ordering (multi-dimensional clustering)”

Z-Ordering is a
technique
 to colocate related information in the same set of files. This co-locality is automatically used by Delta Lake in data-skipping algorithms. This behavior dramatically reduces the amount of data that Delta Lake on Apache Spark needs to read. To Z-Order data, you specify the columns to order on in the
ZORDER BY
 clause:

  SQL

  Python

  Scala

OPTIMIZE events ZORDER
BY
 (eventType)

-- If you have a large amount of data and only want to optimize a subset of it, you can specify an optional partition predicate by using "where".
OPTIMIZE events
WHERE

date

=

'
2021-11-18
'
 ZORDER
BY
 (eventType)

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
# path-based table
# For Hive metastore-based tables: deltaTable = DeltaTable.forName(spark, tableName)

deltaTable.
optimize
().
executeZOrderBy
(
eventType
)

# If you have a large amount of data and only want to optimize a subset of it, you can specify an optional partition predicate using `where`
deltaTable.
optimize
().
where
(
"
date='2021-11-18'
"
).
executeZOrderBy
(
eventType
)

import
 io.delta.tables._

val

deltaTable

=

DeltaTable
.forPath(spark, pathToTable)
// path-based table
// For Hive metastore-based tables: val deltaTable = DeltaTable.forName(spark, tableName)

deltaTable.optimize().executeZOrderBy(eventType)

// If you have a large amount of data and only want to optimize a subset of it, you can specify an optional partition predicate by using "where".
deltaTable.optimize().where(
"
date='2021-11-18'
"
).executeZOrderBy(eventType)

For Scala, Java, and Python API syntax details, see the
Delta Lake APIs

If you expect a column to be commonly used in query predicates and if that column has high cardinality (that is, a large number of distinct values), then use
ZORDER BY
.

You can specify multiple columns for
ZORDER BY
 as a comma-separated list. However, the effectiveness of the locality drops with each extra column. Z-Ordering on columns that do not have statistics collected on them would be ineffective and a waste of resources. This is because data skipping requires column-local stats such as min, max, and count. You can configure statistics collection on certain columns by reordering columns in the schema, or you can increase the number of columns to collect statistics on. See
Data skipping
.

Multi-part checkpointing
Section titled “Multi-part checkpointing”

Delta Lake table periodically and automatically compacts all the incremental updates to the Delta log into a Parquet file. This “checkpointing” allows read queries to quickly reconstruct the current state of the table (that is, which files to process, what is the current schema) without reading too many files having incremental updates.

Delta Lake protocol allows
splitting the checkpoint
 into multiple Parquet files. This parallelizes and speeds up writing the checkpoint. In Delta Lake, by default each classic checkpoint is written as a single Parquet file. For V2 checkpoints, the default part size is 50,000 actions, meaning V2 checkpoint sidecar files are automatically split when the number of actions exceeds this threshold. You can tune this for both classic and V2 checkpoints via the SQL configuration
spark.databricks.delta.checkpoint.partSize=<n>
, where
n
 is the limit of number of actions (such as
AddFile
) at which Delta Lake on Apache Spark will start parallelizing the checkpoint and attempt to write a maximum of this many actions per checkpoint file.

Log compactions
Section titled “Log compactions”

Delta Lake protocol allows new log compaction files with the format
<x>.<y>.compact.json
. These files contain the aggregated actions for commit range
[x, y]
. Log compactions reduce the need for frequent checkpoints and minimize the latency spikes caused by them.

The read support for the log compaction files is available in Delta Lake 3.0.0 and above. It is enabled by default and can be disabled using the SQL conf
spark.databricks.delta.deltaLog.minorCompaction.useForReads=<value>
 where
value
 can be
true/false
. The write support for the log compaction will be added in a future version of Delta.

Optimized Write
Section titled “Optimized Write”

Optimized writes improve file size as data is written and benefit subsequent reads on the table.

Optimized writes are most effective for partitioned tables, as they reduce the number of small files written to each partition. Writing fewer large files is more efficient than writing many small files, but you might still see an increase in write latency because data is shuffled before being written.

The following image demonstrates how optimized writes works:

The optimized write feature is
disabled
 by default. It can be enabled at the table, SQL session, and/or DataFrameWriter level using the following settings (in order of precedence from low to high):

The
delta.autoOptimize.optimizeWrite
 table property (default=None);

The
spark.databricks.delta.optimizeWrite.enabled
 SQL configuration (default=None);

The DataFrameWriter option
optimizeWrite
 (default=None).

Besides the above, the following advanced SQL configurations can be used to further fine-tune the number and size of files written:

spark.databricks.delta.optimizeWrite.binSize
 (default=512MiB), which controls the target in-memory size of each output file;

spark.databricks.delta.optimizeWrite.numShuffleBlocks
 (default=50,000,000), which controls “maximum number of shuffle blocks to target”;

spark.databricks.delta.optimizeWrite.maxShufflePartitions
 (default=2,000), which controls “max number of output buckets (reducers) that can be used by optimized writes”.
