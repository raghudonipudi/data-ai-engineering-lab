# Source: https://docs.delta.io/latest/delta-batch.html

Table batch reads and writes

Delta Lake supports most of the options provided by Apache Spark DataFrame read and write APIs for performing batch reads and writes on tables.

For many Delta Lake operations on tables, you enable integration with Apache Spark DataSourceV2 and Catalog APIs (since 3.0) by setting configurations when you create a new
SparkSession
. See
Configure SparkSession
.

Create a table
Section titled “Create a table”

Delta Lake supports creating two types of tables—tables defined in the metastore and tables defined by path.

To work with metastore-defined tables, you must enable integration with Apache Spark DataSourceV2 and Catalog APIs by setting configurations when you create a new
SparkSession
. See
Configure SparkSession
.

You can create tables in the following ways:

SQL DDL commands
: You can use standard SQL DDL commands supported in Apache Spark (for example,
CREATE TABLE
 and
REPLACE TABLE
) to create Delta tables.

  SQL

CREATE

TABLE

IF

NOT

EXISTS

default
.people10m (

id
INT
,

firstName STRING,

middleName STRING,

lastName STRING,

gender STRING,

birthDate
TIMESTAMP
,

ssn STRING,

salary
INT
)
USING
 DELTA

CREATE OR REPLACE

TABLE

default
.people10m (

id
INT
,

firstName STRING,

middleName STRING,

lastName STRING,

gender STRING,

birthDate
TIMESTAMP
,

ssn STRING,

salary
INT
)
USING
 DELTA

SQL also supports creating a table at a path, without creating an entry in the Hive metastore.

  SQL

-- Create or replace table with path
CREATE OR REPLACE

TABLE

delta
.
`
/tmp/delta/people10m
`
 (

id
INT
,

firstName STRING,

middleName STRING,

lastName STRING,

gender STRING,

birthDate
TIMESTAMP
,

ssn STRING,

salary
INT
)
USING
 DELTA

DataFrameWriter
 API
: If you want to simultaneously create a table and insert data into it from Spark DataFrames or Datasets, you can use the Spark
DataFrameWriter
 (
Scala or Java
 and
Python
).

  Python

  Scala

# Create table in the metastore using DataFrame's schema and write data to it
df.write.
format
(
"
delta
"
).
saveAsTable
(
"
default.people10m
"
)

# Create or replace partitioned table with path using DataFrame's schema and write/overwrite data to it
df.write.
format
(
"
delta
"
).
mode
(
"
overwrite
"
).
save
(
"
/tmp/delta/people10m
"
)

// Create table in the metastore using DataFrame's schema and write data to it
df.write.format(
"
delta
"
).saveAsTable(
"
default.people10m
"
)

// Create table with path using DataFrame's schema and write data to it
df.write.format(
"
delta
"
).mode(
"
overwrite
"
).save(
"
/tmp/delta/people10m
"
)

You can also create Delta tables using the Spark
DataFrameWriterV2
 API.

DeltaTableBuilder
 API
: You can also use the
DeltaTableBuilder
 API in Delta Lake to create tables. Compared to the DataFrameWriter APIs, this API makes it easier to specify additional information like column comments, table properties, and
generated columns
.

See the
API documentation
 for details.

Partition data
Section titled “Partition data”

You can partition data to speed up queries or DML that have predicates involving the partition columns. To partition data when you create a Delta table, specify a partition by columns. The following example partitions by gender.

  SQL

  Python

  Scala

-- Create table in the metastore
CREATE

TABLE

default
.people10m (

id
INT
,

firstName STRING,

middleName STRING,

lastName STRING,

gender STRING,

birthDate
TIMESTAMP
,

ssn STRING,

salary
INT
)
USING
 DELTA
PARTITIONED
BY
 (gender)

df.write.
format
(
"
delta
"
).
partitionBy
(
"
gender
"
).
saveAsTable
(
"
default.people10m
"
)

DeltaTable.
create
(
spark
) \

.
tableName
(
"
default.people10m
"
) \

.
addColumn
(
"
id
"
,

"
INT
"
) \

.
addColumn
(
"
firstName
"
,

"
STRING
"
) \

.
addColumn
(
"
middleName
"
,

"
STRING
"
) \

.
addColumn
(
"
lastName
"
,

"
STRING
"
,

comment

=

"
surname
"
) \

.
addColumn
(
"
gender
"
,

"
STRING
"
) \

.
addColumn
(
"
birthDate
"
,

"
TIMESTAMP
"
) \

.
addColumn
(
"
ssn
"
,

"
STRING
"
) \

.
addColumn
(
"
salary
"
,

"
INT
"
) \

.
partitionedBy
(
"
gender
"
) \

.
execute
()

df.write.format(
"
delta
"
).partitionBy(
"
gender
"
).saveAsTable(
"
default.people10m
"
)

DeltaTable
.createOrReplace(spark)

.tableName(
"
default.people10m
"
)

.addColumn(
"
id
"
,
"
INT
"
)

.addColumn(
"
firstName
"
,
"
STRING
"
)

.addColumn(
"
middleName
"
,
"
STRING
"
)

.addColumn(

DeltaTable
.columnBuilder(
"
lastName
"
)

.dataType(
"
STRING
"
)

.comment(
"
surname
"
)

.build())

.addColumn(
"
lastName
"
,
"
STRING
"
, comment
=

"
surname
"
)

.addColumn(
"
gender
"
,
"
STRING
"
)

.addColumn(
"
birthDate
"
,
"
TIMESTAMP
"
)

.addColumn(
"
ssn
"
,
"
STRING
"
)

.addColumn(
"
salary
"
,
"
INT
"
)

.partitionedBy(
"
gender
"
)

.execute()

To determine whether a table contains a specific partition, use the statement
SELECT COUNT(*) > 0 FROM <table-name> WHERE <partition-column> = <value>
. If the partition exists,
true
 is returned. For example:

  SQL

  Python

  Scala

SELECT

COUNT
(
*
)
>

0

AS

`
Partition exists
`

FROM

default
.people10m
WHERE
 gender
=

"
M
"

display
(
spark.
sql
(
"
SELECT COUNT(*) > 0 AS `Partition exists` FROM default.people10m WHERE gender = 'M'
"
))

display(spark.sql(
"
SELECT COUNT(*) > 0 AS `Partition exists` FROM default.people10m WHERE gender = 'M'
"
))

Control data location
Section titled “Control data location”

For tables defined in the metastore, you can optionally specify the
LOCATION
 as a path. Tables created with a specified
LOCATION
 are considered unmanaged by the metastore. Unlike a managed table, where no path is specified, an unmanaged table’s files are not deleted when you
DROP
 the table.

When you run
CREATE TABLE
 with a
LOCATION
 that
already
 contains data stored using Delta Lake, Delta Lake does the following:

If you specify
only the table name and location
, for example:

  SQL

CREATE

TABLE

default
.people10m
USING
 DELTA
LOCATION

'
/tmp/delta/people10m
'

the table in the metastore automatically inherits the schema, partitioning, and table properties of the existing data. This functionality can be used to “import” data into the metastore.

If you specify
any configuration
 (schema, partitioning, or table properties), Delta Lake verifies that the specification exactly matches the configuration of the existing data.

Use generated columns
Section titled “Use generated columns”

Delta Lake supports generated columns which are a special type of columns whose values are automatically generated based on a user-specified function over other columns in the Delta table. When you write to a table with generated columns and you do not explicitly provide values for them, Delta Lake automatically computes the values. For example, you can automatically generate a date column (for partitioning the table by date) from the timestamp column; any writes into the table need only specify the data for the timestamp column. However, if you explicitly provide values for them, the values must satisfy the
constraint

(<value> <=> <generation expression>) IS TRUE
 or the write will fail with an error.

The following example shows how to create a table with generated columns:

  Python

  Scala

DeltaTable.
create
(
spark
) \

.
tableName
(
"
default.people10m
"
) \

.
addColumn
(
"
id
"
,

"
INT
"
) \

.
addColumn
(
"
firstName
"
,

"
STRING
"
) \

.
addColumn
(
"
middleName
"
,

"
STRING
"
) \

.
addColumn
(
"
lastName
"
,

"
STRING
"
,

comment

=

"
surname
"
) \

.
addColumn
(
"
gender
"
,

"
STRING
"
) \

.
addColumn
(
"
birthDate
"
,

"
TIMESTAMP
"
) \

.
addColumn
(
"
dateOfBirth
"
,

DateType
()
,

generatedAlwaysAs
=
"
CAST(birthDate AS DATE)
"
) \

.
addColumn
(
"
ssn
"
,

"
STRING
"
) \

.
addColumn
(
"
salary
"
,

"
INT
"
) \

.
partitionedBy
(
"
gender
"
) \

.
execute
()

DeltaTable
.create(spark)

.tableName(
"
default.people10m
"
)

.addColumn(
"
id
"
,
"
INT
"
)

.addColumn(
"
firstName
"
,
"
STRING
"
)

.addColumn(
"
middleName
"
,
"
STRING
"
)

.addColumn(

DeltaTable
.columnBuilder(
"
lastName
"
)

.dataType(
"
STRING
"
)

.comment(
"
surname
"
)

.build())

.addColumn(
"
lastName
"
,
"
STRING
"
, comment
=

"
surname
"
)

.addColumn(
"
gender
"
,
"
STRING
"
)

.addColumn(
"
birthDate
"
,
"
TIMESTAMP
"
)

.addColumn(

DeltaTable
.columnBuilder(
"
dateOfBirth
"
)

.dataType(
DateType
)

.generatedAlwaysAs(
"
CAST(dateOfBirth AS DATE)
"
)

.build())

.addColumn(
"
ssn
"
,
"
STRING
"
)

.addColumn(
"
salary
"
,
"
INT
"
)

.partitionedBy(
"
gender
"
)

.execute()

Generated columns are stored as if they were normal columns. That is, they occupy storage.

The following restrictions apply to generated columns:

A generation expression can use any SQL functions in Spark that always return the same result when given the same argument values, except the following types of functions:

User-defined functions.

Aggregate functions.

Window functions.

Functions returning multiple rows.

For Delta Lake 1.1.0 and above,
MERGE
 operations support generated columns when you set
spark.databricks.delta.schema.autoMerge.enabled
 to true.

Delta Lake may be able to generate partition filters for a query whenever a partition column is defined by one of the following expressions:

CAST(col AS DATE)
 and the type of
col
 is
TIMESTAMP
.

YEAR(col)
 and the type of
col
 is
TIMESTAMP
.

Two partition columns defined by
YEAR(col), MONTH(col)
 and the type of
col
 is
TIMESTAMP
.

Three partition columns defined by
YEAR(col), MONTH(col), DAY(col)
 and the type of
col
 is
TIMESTAMP
.

Four partition columns defined by
YEAR(col), MONTH(col), DAY(col), HOUR(col)
 and the type of
col
 is
TIMESTAMP
.

SUBSTRING(col, pos, len)
 and the type of
col
 is
STRING

DATE_FORMAT(col, format)
 and the type of
col
 is
TIMESTAMP
.

DATE_TRUNC(format, col)
 and the type of the
col
 is
TIMESTAMP
 or
DATE
.

TRUNC(col, format)
 and type of the
col
 is either
TIMESTAMP
 or
DATE
.

If a partition column is defined by one of the preceding expressions, and a query filters data using the underlying base column of a generation expression, Delta Lake looks at the relationship between the base column and the generated column, and populates partition filters based on the generated partition column if possible. For example, given the following table:

  Python

DeltaTable.
create
(
spark
) \

.
tableName
(
"
default.events
"
) \

.
addColumn
(
"
eventId
"
,

"
BIGINT
"
) \

.
addColumn
(
"
data
"
,

"
STRING
"
) \

.
addColumn
(
"
eventType
"
,

"
STRING
"
) \

.
addColumn
(
"
eventTime
"
,

"
TIMESTAMP
"
) \

.
addColumn
(
"
eventDate
"
,

"
DATE
"
,

generatedAlwaysAs
=
"
CAST(eventTime AS DATE)
"
) \

.
partitionedBy
(
"
eventType
"
,

"
eventDate
"
) \

.
execute
()

If you then run the following query:

  Python

spark.
sql
(
'
SELECT * FROM default.events WHERE eventTime >= "2020-10-01 00:00:00" <= "2020-10-01 12:00:00"
'
)

Delta Lake automatically generates a partition filter so that the preceding query only reads the data in partition
date=2020-10-01
 even if a partition filter is not specified.

As another example, given the following table:

  Python

DeltaTable.
create
(
spark
) \

.
tableName
(
"
default.events
"
) \

.
addColumn
(
"
eventId
"
,

"
BIGINT
"
) \

.
addColumn
(
"
data
"
,

"
STRING
"
) \

.
addColumn
(
"
eventType
"
,

"
STRING
"
) \

.
addColumn
(
"
eventTime
"
,

"
TIMESTAMP
"
) \

.
addColumn
(
"
year
"
,

"
INT
"
,

generatedAlwaysAs
=
"
YEAR(eventTime)
"
) \

.
addColumn
(
"
month
"
,

"
INT
"
,

generatedAlwaysAs
=
"
MONTH(eventTime)
"
) \

.
addColumn
(
"
day
"
,

"
INT
"
,

generatedAlwaysAs
=
"
DAY(eventTime)
"
) \

.
partitionedBy
(
"
eventType
"
,

"
year
"
,

"
month
"
,

"
day
"
) \

.
execute
()

If you then run the following query:

  Python

spark.
sql
(
'
SELECT * FROM default.events WHERE eventTime >= "2020-10-01 00:00:00" <= "2020-10-01 12:00:00"
'
)

Delta Lake automatically generates a partition filter so that the preceding query only reads the data in partition
year=2020/month=10/day=01
 even if a partition filter is not specified.

You can use an
EXPLAIN
 clause and check the provided plan to see whether Delta Lake automatically generates any partition filters.

Use identity columns
Section titled “Use identity columns”

Delta Lake identity columns are supported in Delta Lake 3.3 and above. They are a type of generated column that assigns unique values for each record inserted into a table. The following example shows how to declare an identity column during a create table command:

  Python

  Scala

from
 delta.tables
import
 DeltaTable, IdentityGenerator
from
 pyspark.sql.types
import
 LongType

DeltaTable.
create
()

.
tableName
(
"
table_name
"
)

.
addColumn
(
"
id_col1
"
,

dataType
=
LongType
()
,

generatedAlwaysAs
=
IdentityGenerator
())

.
addColumn
(
"
id_col2
"
,

dataType
=
LongType
()
,

generatedAlwaysAs
=
IdentityGenerator
(
start
=-
1
,

step
=
1
))

.
addColumn
(
"
id_col3
"
,

dataType
=
LongType
()
,

generatedByDefaultAs
=
IdentityGenerator
())

.
addColumn
(
"
id_col4
"
,

dataType
=
LongType
()
,

generatedByDefaultAs
=
IdentityGenerator
(
start
=-
1
,

step
=
1
))

.
execute
()

import
 io.delta.tables.
DeltaTable
import
 org.apache.spark.sql.types.
LongType

DeltaTable
.create(spark)

.tableName(
"
table_name
"
)

.addColumn(

DeltaTable
.columnBuilder(spark,
"
id_col1
"
)

.dataType(
LongType
)

.generatedAlwaysAsIdentity().build())

.addColumn(

DeltaTable
.columnBuilder(spark,
"
id_col2
"
)

.dataType(
LongType
)

.generatedAlwaysAsIdentity(start
=

-
1L
, step
=

1L
).build())

.addColumn(

DeltaTable
.columnBuilder(spark,
"
id_col3
"
)

.dataType(
LongType
)

.generatedByDefaultAsIdentity().build())

.addColumn(

DeltaTable
.columnBuilder(spark,
"
id_col4
"
)

.dataType(
LongType
)

.generatedByDefaultAsIdentity(start
=

-
1L
, step
=

1L
).build())

.execute()

You can optionally specify the following:

A starting value.

A step size, which can be positive or negative.

Both the starting value and step size default to
1
. You cannot specify a step size of
0
.

Values assigned by identity columns are unique and increment in the direction of the specified step, and in multiples of the specified step size, but are not guaranteed to be contiguous. For example, with a starting value of
0
 and a step size of
2
, all values are positive even numbers but some even numbers might be skipped.

When the identity column is specified to be
generated by default as identity
, insert operations can specify values for the identity column. Specify it to be
generated always as identity
 to override the ability to manually set values.

Identity columns only support
LongType
, and operations fail if the assigned value exceeds the range supported by
LongType
.

You can use
ALTER TABLE table_name ALTER COLUMN column_name SYNC IDENTITY
 to synchronize the metadata of an identity column with the actual data. When you write your own values to an identity column, it might not comply with the metadata. This option evaluates the state and updates the metadata to be consistent with the actual data. After this command, the next automatically assigned identity value will start from
start + (n + 1) * step
, where
n
 is the smallest value that satisfies
start + n * step >= max()
 (for a positive step).

CTAS and identity columns
Section titled “CTAS and identity columns”

You cannot define schema, identity column constraints, or any other table specifications when using a
CREATE TABLE table_name AS SELECT
 (CTAS) statement.

To create a new table with an identity column and populate it with existing data, do the following:

Create a table with the correct schema, including the identity column definition and other table properties.

Run an insertion operation.

The following example define the identity column to be
generated by default as identity
. If data inserted into the table includes valid values for the identity column, these values are used.

  Python

  Scala

from
 delta.tables
import
 DeltaTable, IdentityGenerator
from
 pyspark.sql.types
import
 LongType, DateType

DeltaTable.
create
(
spark
)

.
tableName
(
"
new_table
"
)

.
addColumn
(
"
id
"
,

dataType
=
LongType
()
,

generatedByDefaultAs
=
IdentityGenerator
(
start
=
5
,

step
=
1
))

.
addColumn
(
"
event_date
"
,

dataType
=
DateType
())

.
addColumn
(
"
some_value
"
,

dataType
=
LongType
())

.
execute
()

# Insert records including existing IDs
old_table_df
=
 spark.
table
(
"
old_table
"
).
select
(
"
id
"
,

"
event_date
"
,

"
some_value
"
)
old_table_df.write

.
format
(
"
delta
"
)

.
mode
(
"
append
"
)

.
saveAsTable
(
"
new_table
"
)

# Insert records and generate new IDs
new_records_df
=
 spark.
table
(
"
new_records
"
).
select
(
"
event_date
"
,

"
some_value
"
)
new_records_df.write

.
format
(
"
delta
"
)

.
mode
(
"
append
"
)

.
saveAsTable
(
"
new_table
"
)

import
 org.apache.spark.sql.types._
import
 io.delta.tables.
DeltaTable

DeltaTable
.createOrReplace(spark)

.tableName(
"
new_table
"
)

.addColumn(

DeltaTable
.columnBuilder(spark,
"
id
"
)

.dataType(
LongType
)

.generatedByDefaultAsIdentity(start
=

5L
, step
=

1L
)

.build())

.addColumn(

DeltaTable
.columnBuilder(spark,
"
event_date
"
)

.dataType(
DateType
)

.nullable(
true
)

.build())

.addColumn(

DeltaTable
.columnBuilder(spark,
"
some_value
"
)

.dataType(
LongType
)

.nullable(
true
)

.build())

.execute()

// Insert records including existing IDs
val

oldTableDF

=
 spark.table(
"
old_table
"
).select(
"
id
"
,
"
event_date
"
,
"
some_value
"
)
oldTableDF.write

.format(
"
delta
"
)

.mode(
"
append
"
)

.saveAsTable(
"
new_table
"
)

// Insert records and generate new IDs
val

newRecordsDF

=
 spark.table(
"
new_records
"
).select(
"
event_date
"
,
"
some_value
"
)
newRecordsDF.write

.format(
"
delta
"
)

.mode(
"
append
"
)

.saveAsTable(
"
new_table
"
)

Identity column limitations
Section titled “Identity column limitations”

The following limitations exist when working with identity columns:

Concurrent transactions are not supported on tables with identity columns enabled.

You cannot partition a table by an identity column.

You cannot
ADD
,
REPLACE
, or
CHANGE
 an identity column.

You cannot update the value of an identity column for an existing record.

Specify default values for columns
Section titled “Specify default values for columns”

Delta enables the specification of
default expressions
 for columns in Delta tables. When users write to these tables without explicitly providing values for certain columns, or when they explicitly use the
DEFAULT
 SQL keyword for a column, Delta automatically generates default values for those columns. For more information, please refer to the dedicated documentation page.

Use special characters in column names
Section titled “Use special characters in column names”

By default, special characters such as spaces and any of the characters
,;{}()\n\t=
 are not supported in table column names. To include these special characters in a table’s column name, enable column mapping.

Default table properties
Section titled “Default table properties”

Delta Lake configurations set in the SparkSession override the default
table properties
 for new Delta Lake tables created in the session. The prefix used in the SparkSession is different from the configurations used in the table properties.

Delta Lake conf
SparkSession conf
delta.<conf>
spark.databricks.delta.properties.defaults.<conf>

For example, to set the
delta.appendOnly = true
 property for all new Delta Lake tables created in a session, set the following:

SET

spark
.
databricks
.
delta
.
properties
.
defaults
.
appendOnly

=
 true

Read a table
Section titled “Read a table”

You can load a Delta table as a DataFrame by specifying a table name or a path:

  SQL

  Python

  Scala

SELECT

*

FROM

default
.people10m
-- query table in the metastore

SELECT

*

FROM
 delta.
`
/tmp/delta/people10m
`

-- query table by path

spark.
table
(
"
default.people10m
"
)
# query table in the metastore

spark.read.
format
(
"
delta
"
).
load
(
"
/tmp/delta/people10m
"
)
# query table by path

spark.table(
"
default.people10m
"
)
// query table in the metastore

spark.read.format(
"
delta
"
).load(
"
/tmp/delta/people10m
"
)
// create table by path

import
 io.delta.implicits._
spark.read.delta(
"
/tmp/delta/people10m
"
)

The DataFrame returned automatically reads the most recent snapshot of the table for any query; you never need to run
REFRESH TABLE
. Delta Lake automatically uses partitioning and statistics to read the minimum amount of data when there are applicable predicates in the query.

Query an older snapshot of a table (time travel)
Section titled “Query an older snapshot of a table (time travel)”

Delta Lake time travel allows you to query an older snapshot of a Delta table. Time travel has many use cases, including:

Re-creating analyses, reports, or outputs (for example, the output of a machine learning model). This could be useful for debugging or auditing, especially in regulated industries.

Writing complex temporal queries.

Fixing mistakes in your data.

Providing snapshot isolation for a set of queries for fast changing tables.

This section describes the supported methods for querying older versions of tables, data retention concerns, and provides examples.

Syntax
Section titled “Syntax”

This section shows how to query an older version of a Delta table.

SQL
AS OF
 syntax
Section titled “SQL AS OF syntax”

  SQL

SELECT

*

FROM
 table_name
TIMESTAMP

AS
 OF timestamp_expression
SELECT

*

FROM
 table_name
VERSION

AS
 OF
version

timestamp_expression
 can be any one of:

'2018-10-18T22:15:12.013Z'
, that is, a string that can be cast to a timestamp

cast('2018-10-18 13:36:32 CEST' as timestamp)

'2018-10-18'
, that is, a date string

current_timestamp() - interval 12 hours

date_sub(current_date(), 1)

Any other expression that is or can be cast to a timestamp

version
 is a long value that can be obtained from the output of
DESCRIBE HISTORY table_spec
.

Neither
timestamp_expression
 nor
version
 can be subqueries.

Example
Section titled “Example”

  SQL

SELECT

*

FROM

default
.people10m
TIMESTAMP

AS
 OF
'
2018-10-18T22:15:12.013Z
'
SELECT

*

FROM
 delta.
`
/tmp/delta/people10m
`

VERSION

AS
 OF
123

DataFrameReader options
Section titled “DataFrameReader options”

DataFrameReader options allow you to create a DataFrame from a Delta table that is fixed to a specific version of the table.

  Python

df1
=
 spark.read.
format
(
"
delta
"
).
option
(
"
timestampAsOf
"
,
 timestamp_string
).
load
(
"
/tmp/delta/people10m
"
)
df2
=
 spark.read.
format
(
"
delta
"
).
option
(
"
versionAsOf
"
,
 version
).
load
(
"
/tmp/delta/people10m
"
)

For
timestamp_string
, only date or timestamp strings are accepted. For example,
"2019-01-01"
 and
"2019-01-01T00:00:00.000Z"
.

A common pattern is to use the latest state of the Delta table throughout the execution of a job to update downstream applications.

Because Delta tables auto update, a DataFrame loaded from a Delta table may return different results across invocations if the underlying data is updated. By using time travel, you can fix the data returned by the DataFrame across invocations:

  Python

history
=
 spark.
sql
(
"
DESCRIBE HISTORY delta.`/tmp/delta/people10m`
"
)
latest_version
=
 history.
selectExpr
(
"
max(version)
"
).
collect
()
df
=
 spark.read.
format
(
"
delta
"
).
option
(
"
versionAsOf
"
,
 latest_version
[
0
]
[
0
]
).
load
(
"
/tmp/delta/people10m
"
)

Examples
Section titled “Examples”

Fix accidental deletes to a table for the user 111:

  Python

yesterday
=
 spark.
sql
(
"
SELECT CAST(date_sub(current_date(), 1) AS STRING)
"
).
collect
()
[
0
][
0
]
df
=
 spark.read.
format
(
"
delta
"
).
option
(
"
timestampAsOf
"
,
 yesterday
).
load
(
"
/tmp/delta/events
"
)
df.
where
(
"
userId = 111
"
).write.
format
(
"
delta
"
).
mode
(
"
append
"
).
save
(
"
/tmp/delta/events
"
)

Fix accidental incorrect updates to a table:

  Python

yesterday
=
 spark.
sql
(
"
SELECT CAST(date_sub(current_date(), 1) AS STRING)
"
).
collect
()
[
0
][
0
]
df
=
 spark.read.
format
(
"
delta
"
).
option
(
"
timestampAsOf
"
,
 yesterday
).
load
(
"
/tmp/delta/events
"
)
df.
createOrReplaceTempView
(
"
my_table_yesterday
"
)
spark.
sql
(
'''
MERGE INTO delta.`/tmp/delta/events` target

USING my_table_yesterday source

ON source.userId = target.userId

WHEN MATCHED THEN UPDATE SET *
'''
)

Query the number of new customers added over the last week:

  Python

last_week
=
 spark.
sql
(
"
SELECT CAST(date_sub(current_date(), 7) AS STRING)
"
).
collect
()
[
0
][
0
]
df
=
 spark.read.
format
(
"
delta
"
).
option
(
"
timestampAsOf
"
,
 last_week
).
load
(
"
/tmp/delta/events
"
)
last_week_count
=
 df.
select
(
"
userId
"
).
distinct
().
count
()
count
=
 spark.read.
format
(
"
delta
"
).
load
(
"
/tmp/delta/events
"
).
select
(
"
userId
"
).
distinct
().
count
()
new_customers_count
=
 count
-
 last_week_count

Data retention
Section titled “Data retention”

To time travel to a previous version, you must retain
both
 the log and the data files for that version.

The data files backing a Delta table are
never
 deleted automatically; data files are deleted only when you run
VACUUM
.
VACUUM

does not
 delete Delta log files; log files are automatically cleaned up after checkpoints are written.

By default you can time travel to a Delta table up to 30 days old unless you have:

Run
VACUUM
 on your Delta table.

Changed the data or log file retention periods using the following
table properties
:

delta.logRetentionDuration = "interval <interval>"
: controls how long the history for a table is kept. The default is
interval 30 days
.

Each time a checkpoint is written, Delta automatically cleans up log entries older than the retention interval. If you set this config to a large enough value, many log entries are retained. This should not impact performance as operations against the log are constant time. Operations on history are parallel but will become more expensive as the log size increases.

delta.deletedFileRetentionDuration = "interval <interval>"
: controls how long ago a file must have been deleted
before being a candidate for

VACUUM
. The default is
interval 7 days
.

To access 30 days of historical data even if you run
VACUUM
 on the Delta table, set
delta.deletedFileRetentionDuration = "interval 30 days"
. This setting may cause your storage costs to go up.

Write to table
Section titled “Write to table”

Append
Section titled “Append”

To atomically add new data to an existing Delta table, use
append
 mode:

  SQL

  Python

  Scala

INSERT INTO

default
.people10m
SELECT

*

FROM
 morePeople

df.write.
format
(
"
delta
"
).
mode
(
"
append
"
).
save
(
"
/tmp/delta/people10m
"
)
df.write.
format
(
"
delta
"
).
mode
(
"
append
"
).
saveAsTable
(
"
default.people10m
"
)

df.write.format(
"
delta
"
).mode(
"
append
"
).save(
"
/tmp/delta/people10m
"
)
df.write.format(
"
delta
"
).mode(
"
append
"
).saveAsTable(
"
default.people10m
"
)

import
 io.delta.implicits._
df.write.mode(
"
append
"
).delta(
"
/tmp/delta/people10m
"
)

Overwrite
Section titled “Overwrite”

To atomically replace all the data in a table, use
overwrite
 mode:

  SQL

  Python

  Scala

INSERT
 OVERWRITE
TABLE

default
.people10m
SELECT

*

FROM
 morePeople

df.write.
format
(
"
delta
"
).
mode
(
"
overwrite
"
).
save
(
"
/tmp/delta/people10m
"
)
df.write.
format
(
"
delta
"
).
mode
(
"
overwrite
"
).
saveAsTable
(
"
default.people10m
"
)

df.write.format(
"
delta
"
).mode(
"
overwrite
"
).save(
"
/tmp/delta/people10m
"
)
df.write.format(
"
delta
"
).mode(
"
overwrite
"
).saveAsTable(
"
default.people10m
"
)

import
 io.delta.implicits._
df.write.mode(
"
overwrite
"
).delta(
"
/tmp/delta/people10m
"
)

Delta Lake provides several options to selectively overwrite only part of a table. The following table summarizes them. For most use cases, we recommend using
replaceUsing
 or
replaceWhere
. Use
replaceOn
 only when your use case requires complex or null-safe matching conditions.

Option
Use case
Available since
replaceWhere
Atomically overwrite rows that match a predicate. Use for replacements with a fixed matching condition, such as
colA = 5
 or
int_col IN (1, 2, 3)
.
Delta Lake 1.1.0 (DataFrames); 2.4.0 (SQL)
replaceUsing
Dynamic data overwrite by column equality. Replaces all rows that match the specified columns, based on equality comparison of the column values, in the provided data set.
Delta Lake 4.3.0
replaceOn
Dynamic data overwrite by Boolean expression. Use for replacements with a complex or null-safe matching condition, such as
s.colA <=> t.colA AND s.colB <=> t.colB
.
Delta Lake 4.3.0
partitionOverwriteMode
Dynamic partition overwrite, which overwrites all the existing data in each partition for which the write will commit new data. Legacy since Delta Lake 4.3.0; not recommended for new workloads.
Delta Lake 2.0

Overwrite rows matching a predicate with
replaceWhere
Section titled “Overwrite rows matching a predicate with replaceWhere”

replaceWhere
 atomically overwrites the rows that match a predicate, leaving all other rows unchanged. Use it for replacements with a fixed matching condition, such as
colA = 5
 or
int_col IN (1, 2, 3)
. This feature is available with DataFrames in Delta Lake 1.1.0 and above and supported in SQL in Delta Lake 2.4.0 and above.

The following command atomically replaces events in January in the target table, which is partitioned by
start_date
, with the data in
replace_data
:

  SQL

  Python

  Scala

INSERT INTO

TABLE
 events
REPLACE

WHERE
 start_data
>=

'
2017-01-01
'

AND
 end_date
<=

'
2017-01-31
'

SELECT

*

FROM
 replace_data

replace_data.write \

.
format
(
"
delta
"
) \

.
mode
(
"
overwrite
"
) \

.
option
(
"
replaceWhere
"
,

"
start_date >= '2017-01-01' AND end_date <= '2017-01-31'
"
) \

.
save
(
"
/tmp/delta/events
"
)

replace_data.write

.format(
"
delta
"
)

.mode(
"
overwrite
"
)

.option(
"
replaceWhere
"
,
"
start_date >= '2017-01-01' AND end_date <= '2017-01-31'
"
)

.save(
"
/tmp/delta/events
"
)

This sample code writes out the data in
replace_data
, validates that it all matches the predicate, and performs an atomic replacement. If you want to write out data that doesn’t all match the predicate, to replace the matching rows in the target table, you can disable the constraint check by setting
spark.databricks.delta.replaceWhere.constraintCheck.enabled
 to false:

  SQL

  Python

  Scala

SET

spark
.
databricks
.
delta
.
replaceWhere
.
constraintCheck
.
enabled
=
false

spark.conf.
set
(
"
spark.databricks.delta.replaceWhere.constraintCheck.enabled
"
,

False
)

spark.conf.set(
"
spark.databricks.delta.replaceWhere.constraintCheck.enabled
"
,
false
)

In Delta Lake 1.0.0 and below,
replaceWhere
 overwrites data matching a predicate over partition columns only. The following command atomically replaces the month in January in the target table, which is partitioned by
date
, with the data in
df
:

  Python

  Scala

df.write \

.
format
(
"
delta
"
) \

.
mode
(
"
overwrite
"
) \

.
option
(
"
replaceWhere
"
,

"
birthDate >= '2017-01-01' AND birthDate <= '2017-01-31'
"
) \

.
save
(
"
/tmp/delta/people10m
"
)

df.write

.format(
"
delta
"
)

.mode(
"
overwrite
"
)

.option(
"
replaceWhere
"
,
"
birthDate >= '2017-01-01' AND birthDate <= '2017-01-31'
"
)

.save(
"
/tmp/delta/people10m
"
)

In Delta Lake 1.1.0 and above, if you want to fall back to the old behavior, you can disable the
spark.databricks.delta.replaceWhere.dataColumns.enabled
 flag:

  SQL

  Python

  Scala

SET

spark
.
databricks
.
delta
.
replaceWhere
.
dataColumns
.
enabled
=
false

spark.conf.
set
(
"
spark.databricks.delta.replaceWhere.dataColumns.enabled
"
,

False
)

spark.conf.set(
"
spark.databricks.delta.replaceWhere.dataColumns.enabled
"
,
false
)

Dynamically overwrite data with
replaceUsing
 and
replaceOn
Section titled “Dynamically overwrite data with replaceUsing and replaceOn”

Dynamic data overwrites selectively replace the data that matches the specified key columns or Boolean expression, leaving all other data unchanged. The
replaceUsing
 option matches on key columns, while
replaceOn
 matches on a Boolean expression. Partitioned tables, unpartitioned tables, and tables with liquid clustering are all supported. Both options are available with DataFrames in Delta Lake 4.3.0 and above.

Dynamic partition overwrites (the legacy
partitionOverwriteMode
 option) are a subset of dynamic data overwrite behavior. Dynamic partition overwrites replace all the existing data in each partition for which the write will commit new data, and leave all other partitions unchanged. Only partitioned tables are supported in dynamic partition overwrite mode.

replaceUsing
Section titled “replaceUsing”

replaceUsing
 atomically deletes the rows in the target table that match a row in the incoming DataFrame on the specified columns, then inserts the incoming DataFrame rows. Matching is based on equality comparison of the specified column values. Provide a comma-separated list of columns. Each column must exist in both the table and the incoming DataFrame, at the same ordinal position. The following command replaces rows whose
event_id
 and
start_date
 match between the incoming DataFrame and the target table:

  Python

  Scala

source_data.write \

.
format
(
"
delta
"
) \

.
mode
(
"
overwrite
"
) \

.
option
(
"
replaceUsing
"
,

"
event_id, start_date
"
) \

.
saveAsTable
(
"
events
"
)

source_data.write

.format(
"
delta
"
)

.mode(
"
overwrite
"
)

.option(
"
replaceUsing
"
,
"
event_id, start_date
"
)

.saveAsTable(
"
events
"
)

If the source query is empty, no data is deleted.

Like a
JOIN USING
,
replaceUsing
 matches rows with regular equality, where
NULL
 is not equal to anything. Rows with
NULL
 values in the specified columns don’t match and aren’t removed from the target table. For null-safe matching, or other logic that equality cannot express, use
replaceOn
 instead.

For example, suppose the
students
 table is clustered by
country
:

name
country
Dylan
US
Doug
UK
Julia
IT
Adam
NULL

and the
new_students
 DataFrame holds the replacement rows:

name
country
Peter
FR
Jennie
UK
Eva
NULL

  Python

  Scala

# Replace rows in students whose country matches a row in new_students.
new_students.write \

.
format
(
"
delta
"
) \

.
mode
(
"
overwrite
"
) \

.
option
(
"
replaceUsing
"
,

"
country
"
) \

.
saveAsTable
(
"
students
"
)

// Replace rows in students whose country matches a row in new_students.
new_students.write

.format(
"
delta
"
)

.mode(
"
overwrite
"
)

.option(
"
replaceUsing
"
,
"
country
"
)

.saveAsTable(
"
students
"
)

After the write,
students
 contains:

name
country
Dylan
US
Julia
IT
Jennie
UK
Peter
FR
Adam
NULL
Eva
NULL

Doug
 is removed because
UK
 matches a row in the incoming DataFrame.
Adam
 keeps his row because his
NULL
 country never matches, and
Eva
’s
NULL
 row is appended for the same reason.

replaceOn
Section titled “replaceOn”

replaceOn
 replaces rows when they match a user-defined condition, unlike
replaceUsing
, which replaces rows when the specified columns compare equal under equality. Use
replaceOn
 when you need matching logic that
replaceUsing
 does not support, such as treating
NULL
 values as equal with the
<=>
 operator.

Optionally, use the
targetAlias
 option to specify an alias for the target table and the
.as()
 or
.alias()
 APIs to specify an alias for the source data.

The following command replaces rows whose
event_id
 and
start_date
 match between the incoming DataFrame and the target table:

  Python

  Scala

source_data.
alias
(
"
s
"
).write \

.
format
(
"
delta
"
) \

.
mode
(
"
overwrite
"
) \

.
option
(
"
targetAlias
"
,

"
t
"
) \

.
option
(
"
replaceOn
"
,

"
s.event_id <=> t.event_id AND s.start_date <=> t.start_date
"
) \

.
saveAsTable
(
"
events
"
)

source_data.as(
"
s
"
).write

.format(
"
delta
"
)

.mode(
"
overwrite
"
)

.option(
"
targetAlias
"
,
"
t
"
)

.option(
"
replaceOn
"
,
"
s.event_id <=> t.event_id AND s.start_date <=> t.start_date
"
)

.saveAsTable(
"
events
"
)

If the source query is empty, no data is deleted.

For example, suppose the
students
 table contains:

name
row_origin
Alice
table
NULL
table
Bob
table

and the
people
 DataFrame holds the replacement rows:

name
row_origin
Alice
query
NULL
query
Delta
query

  Python

  Scala

# Replace rows in students whose name matches a row in people, using a null-safe comparison.
people.
alias
(
"
s
"
).write \

.
format
(
"
delta
"
) \

.
mode
(
"
overwrite
"
) \

.
option
(
"
targetAlias
"
,

"
t
"
) \

.
option
(
"
replaceOn
"
,

"
t.name <=> s.name
"
) \

.
saveAsTable
(
"
students
"
)

// Replace rows in students whose name matches a row in people, using a null-safe comparison.
people.as(
"
s
"
).write

.format(
"
delta
"
)

.mode(
"
overwrite
"
)

.option(
"
targetAlias
"
,
"
t
"
)

.option(
"
replaceOn
"
,
"
t.name <=> s.name
"
)

.saveAsTable(
"
students
"
)

After the write,
students
 contains:

name
row_origin
Alice
query
NULL
query
Bob
table
Delta
query

Because
<=>
 is null-safe, the
NULL
 row matches and is replaced.
Bob
 has no match in the incoming DataFrame, so his row is kept, and
Delta
 is appended.

Dynamic Partition Overwrites with
partitionOverwriteMode
 (legacy since Delta Lake 4.3.0)
Section titled “Dynamic Partition Overwrites with partitionOverwriteMode (legacy since Delta Lake 4.3.0)”

Delta Lake 2.0 and above supports
dynamic
 partition overwrite mode for partitioned tables.

When in dynamic partition overwrite mode, we overwrite all existing data in each logical partition for which the write will commit new data. Any existing logical partitions for which the write does not contain data will remain unchanged. This mode is only applicable when data is being written in overwrite mode: either
INSERT OVERWRITE
 in SQL, or a DataFrame write with
df.write.mode("overwrite")
.

Configure dynamic partition overwrite mode by setting the Spark session configuration
spark.sql.sources.partitionOverwriteMode
 to
dynamic
. You can also enable this by setting the
DataFrameWriter
 option
partitionOverwriteMode
 to
dynamic
. If present, the query-specific option overrides the mode defined in the session configuration. The default for
partitionOverwriteMode
 is
static
.

  SQL

  Python

  Scala

SET

spark
.
sql
.
sources
.
partitionOverwriteMode
=dynamic
;
INSERT
 OVERWRITE
TABLE

default
.people10m
SELECT

*

FROM
 morePeople;

df.write \

.
format
(
"
delta
"
) \

.
mode
(
"
overwrite
"
) \

.
option
(
"
partitionOverwriteMode
"
,

"
dynamic
"
) \

.
saveAsTable
(
"
default.people10m
"
)

df.write

.format(
"
delta
"
)

.mode(
"
overwrite
"
)

.option(
"
partitionOverwriteMode
"
,
"
dynamic
"
)

.saveAsTable(
"
default.people10m
"
)

For Delta Lake support for updating tables, see
Table deletes, updates, and merges
.

Limit rows written in a file
Section titled “Limit rows written in a file”

You can use the SQL session configuration
spark.sql.files.maxRecordsPerFile
 to specify the maximum number of records to write to a single file for a Delta Lake table. Specifying a value of zero or a negative value represents no limit.

You can also use the DataFrameWriter option
maxRecordsPerFile
 when using the DataFrame APIs to write to a Delta Lake table. When
maxRecordsPerFile
 is specified, the value of the SQL session configuration
spark.sql.files.maxRecordsPerFile
 is ignored.

  Python

  Scala

df.write.
format
(
"
delta
"
) \

.
mode
(
"
append
"
) \

.
option
(
"
maxRecordsPerFile
"
,

"
10000
"
) \

.
save
(
"
/tmp/delta/people10m
"
)

df.write.format(
"
delta
"
)

.mode(
"
append
"
)

.option(
"
maxRecordsPerFile
"
,
"
10000
"
)

.save(
"
/tmp/delta/people10m
"
)

Idempotent writes
Section titled “Idempotent writes”

Sometimes a job that writes data to a Delta table is restarted due to various reasons (for example, job encounters a failure). The failed job may or may not have written the data to Delta table before terminating. In the case where the data is written to the Delta table, the restarted job writes the same data to the Delta table which results in duplicate data.

To address this, Delta tables support the following
DataFrameWriter
 options to make the writes idempotent:

txnAppId
: A unique string that you can pass on each
DataFrame
 write. For example, this can be the name of the job.

txnVersion
: A monotonically increasing number that acts as transaction version. This number needs to be unique for data that is being written to the Delta table(s). For example, this can be the epoch seconds of the instant when the query is attempted for the first time. Any subsequent restarts of the same job needs to have the same value for
txnVersion
.

The above combination of options needs to be unique for each new data that is being ingested into the Delta table and the
txnVersion
 needs to be higher than the last data that was ingested into the Delta table. For example:

Last successfully written data contains option values as
dailyETL:23423
 (
txnAppId:txnVersion
).

Next write of data should have
txnAppId = dailyETL
 and
txnVersion
 as at least
23424
 (one more than the last written data
txnVersion
).

Any attempt to write data with
txnAppId = dailyETL
 and
txnVersion
 as
23422
 or less is ignored because the
txnVersion
 is less than the last recorded
txnVersion
 in the table.

Attempt to write data with
txnAppId:txnVersion
 as
anotherETL:23424
 is successful writing data to the table as it contains a different
txnAppId
 compared to the same option value in last ingested data.

You can also configure idempotent writes by setting the Spark session configuration
spark.databricks.delta.write.txnAppId
 and
spark.databricks.delta.write.txnVersion
. In addition, you can set
spark.databricks.delta.write.txnVersion.autoReset.enabled
 to true to automatically reset
spark.databricks.delta.write.txnVersion
 after every write. When both the writer options and session configuration are set, we will use the writer option values.

Example
Section titled “Example”

  SQL

  Python

  Scala

SET

spark
.
databricks
.
delta
.
write
.txnAppId
=
 ...;
SET

spark
.
databricks
.
delta
.
write
.txnVersion
=
 ...;
SET

spark
.
databricks
.
delta
.
write
.
txnVersion
.
autoReset
.
enabled

=
 true;
-- if set to true, this will reset txnVersion after every write

app_id
=

...

# A unique string that is used as an application ID.
version
=

...

# A monotonically increasing number that acts as transaction version.

dataFrame.write.
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
 version
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

val

appId

=
 ...
// A unique string that is used as an application ID.
version
=
 ...
// A monotonically increasing number that acts as transaction version.

dataFrame.write.format(...).option(
"
txnVersion
"
, version).option(
"
txnAppId
"
, appId).save(...)

Set user-defined commit metadata
Section titled “Set user-defined commit metadata”

You can specify user-defined strings as metadata in commits made by these operations, either using the DataFrameWriter option
userMetadata
 or the SparkSession configuration
spark.databricks.delta.commitInfo.userMetadata
. If both of them have been specified, then the option takes preference. This user-defined metadata is readable in the
history
 operation.

  SQL

  Python

  Scala

SET

spark
.
databricks
.
delta
.
commitInfo
.userMetadata
=
overwritten
-
for
-
fixing
-
incorrect
-
data
INSERT
 OVERWRITE
default
.people10m
SELECT

*

FROM
 morePeople

df.write.
format
(
"
delta
"
) \

.
mode
(
"
overwrite
"
) \

.
option
(
"
userMetadata
"
,

"
overwritten-for-fixing-incorrect-data
"
) \

.
save
(
"
/tmp/delta/people10m
"
)

df.write.format(
"
delta
"
)

.mode(
"
overwrite
"
)

.option(
"
userMetadata
"
,
"
overwritten-for-fixing-incorrect-data
"
)

.save(
"
/tmp/delta/people10m
"
)

Schema validation
Section titled “Schema validation”

Delta Lake automatically validates that the schema of the DataFrame being written is compatible with the schema of the table. Delta Lake uses the following rules to determine whether a write from a DataFrame to a table is compatible:

All DataFrame columns must exist in the target table. If there are columns in the DataFrame not present in the table, an exception is raised. Columns present in the table but not in the DataFrame are set to null.

DataFrame column data types must match the column data types in the target table. If they don’t match, an exception is raised.

DataFrame column names cannot differ only by case. This means that you cannot have columns such as “Foo” and “foo” defined in the same table. While you can use Spark in case sensitive or insensitive (default) mode, Parquet is case sensitive when storing and returning column information. Delta Lake is case-preserving but insensitive when storing the schema and has this restriction to avoid potential mistakes, data corruption, or loss issues.

Delta Lake support DDL to add new columns explicitly and the ability to update schema automatically.

If you specify other options, such as
partitionBy
, in combination with append mode, Delta Lake validates that they match and throws an error for any mismatch. When
partitionBy
 is not present, appends automatically follow the partitioning of the existing data.

Update table schema
Section titled “Update table schema”

Delta Lake lets you update the schema of a table. The following types of changes are supported:

Adding new columns (at arbitrary positions)

Reordering existing columns

You can make these changes explicitly using DDL or implicitly using DML.

Explicitly update schema
Section titled “Explicitly update schema”

You can use the following DDL to explicitly change the schema of a table.

Add columns
Section titled “Add columns”

  SQL

ALTER

TABLE
 table_name
ADD
 COLUMNS (col_name data_type [COMMENT col_comment] [FIRST|AFTER colA_name], ...)

By default, nullability is
true
.

To add a column to a nested field, use:

  SQL

ALTER

TABLE
 table_name
ADD
 COLUMNS (
col_name
.
nested_col_name
 data_type [COMMENT col_comment] [FIRST|AFTER colA_name], ...)

Example
Section titled “Example”

If the schema before running
ALTER TABLE boxes ADD COLUMNS (colB.nested STRING AFTER field1)
 is:

- root
| - colA
| - colB
| +-field1
| +-field2

the schema after is:

- root
| - colA
| - colB
| +-field1
| +-nested
| +-field2

Change column comment or ordering
Section titled “Change column comment or ordering”

  SQL

ALTER

TABLE
 table_name
ALTER
 [COLUMN] col_name col_name data_type [COMMENT col_comment] [FIRST|AFTER colA_name]

To change a column in a nested field, use:

  SQL

ALTER

TABLE
 table_name
ALTER
 [COLUMN]
col_name
.
nested_col_name
 nested_col_name data_type [COMMENT col_comment] [FIRST|AFTER colA_name]

Example
Section titled “Example”

If the schema before running
ALTER TABLE boxes CHANGE COLUMN colB.field2 field2 STRING FIRST
 is:

- root
| - colA
| - colB
| +-field1
| +-field2

the schema after is:

- root
| - colA
| - colB
| +-field2
| +-field1

Replace columns
Section titled “Replace columns”

  SQL

ALTER

TABLE
 table_name
REPLACE
 COLUMNS (col_name1 col_type1 [COMMENT col_comment1], ...)

Example
Section titled “Example”

When running the following DDL:

  SQL

ALTER

TABLE
 boxes
REPLACE
 COLUMNS (colC STRING, colB STRUCT
<
field2:STRING, nested:STRING, field1:STRING
>
, colA STRING)

if the schema before is:

- root
| - colA
| - colB
| +-field1
| +-field2

the schema after is:

- root
| - colC
| - colB
| +-field2
| +-nested
| +-field1
| - colA

Rename columns
Section titled “Rename columns”

To rename columns without rewriting any of the columns’ existing data, you must enable column mapping for the table. See
enable column mapping
.

To rename a column:

  SQL

ALTER

TABLE
 table_name RENAME COLUMN old_col_name
TO
 new_col_name

To rename a nested field:

  SQL

ALTER

TABLE
 table_name RENAME COLUMN
col_name
.
old_nested_field

TO
 new_nested_field

Example
Section titled “Example”

When you run the following command:

ALTER

TABLE
 boxes RENAME COLUMN
colB
.
field1

TO
 field001

If the schema before is:

- root
| - colA
| - colB
| +-field1
| +-field2

Then the schema after is:

- root
| - colA
| - colB
| +-field001
| +-field2

Drop columns
Section titled “Drop columns”

To drop columns as a metadata-only operation without rewriting any data files, you must enable column mapping for the table. See
enable column mapping
.

To drop a column:

  SQL

ALTER

TABLE
 table_name
DROP
 COLUMN col_name

To drop multiple columns:

  SQL

ALTER

TABLE
 table_name
DROP
 COLUMNS (col_name_1, col_name_2)

Change column type or name
Section titled “Change column type or name”

You can change a column’s type or name or drop a column by rewriting the table. To do this, use the
overwriteSchema
 option:

Change a column type
Section titled “Change a column type”

  Python

spark.read.
table
(
...
) \

.
withColumn
(
"
birthDate
"
,

col
(
"
birthDate
"
)
.
cast
(
"
date
"
)) \

.write \

.
format
(
"
delta
"
) \

.
mode
(
"
overwrite
"
)

.
option
(
"
overwriteSchema
"
,

"
true
"
) \

.
saveAsTable
(
...
)

Change a column name
Section titled “Change a column name”

  Python

spark.read.
table
(
...
) \

.
withColumnRenamed
(
"
dateOfBirth
"
,

"
birthDate
"
) \

.write \

.
format
(
"
delta
"
) \

.
mode
(
"
overwrite
"
) \

.
option
(
"
overwriteSchema
"
,

"
true
"
) \

.
saveAsTable
(
...
)

Automatic schema update
Section titled “Automatic schema update”

Delta Lake can automatically update the schema of a table as part of a DML transaction (either appending or overwriting), and make the schema compatible with the data being written.

Add columns
Section titled “Add columns”

Columns present in the source data but missing from the table are automatically added during a write transaction when schema evolution is enabled. The added columns are appended to the end of the struct they are present in. The case is preserved when a new column is appended.

Enable schema evolution (Delta Lake 4.3 and above)
Section titled “Enable schema evolution (Delta Lake 4.3 and above)”

On Delta Lake 4.3 and above, use
WITH SCHEMA EVOLUTION
 in a SQL
INSERT
 statement or
.withSchemaEvolution()
 in the DataFrame API to enable automatic schema evolution for a single operation. When enabled, the schema of the target Delta Lake table is automatically updated to accommodate additional columns or widened types of the source data. For a list of the supported type changes, see
Supported type changes
. For example:

  SQL

  Python

  Scala

INSERT

WITH

SCHEMA
 EVOLUTION
INTO
 target_table
SELECT

*

FROM
 source_table

(spark.read

.
table
(
"
source_table
"
)

.write

.
mode
(
"
append
"
)

.
withSchemaEvolution
()

.
saveAsTable
(
"
target_table
"
)
)

spark.read

.table(
"
source_table
"
)

.write

.mode(
"
append
"
)

.withSchemaEvolution()

.saveAsTable(
"
target_table
"
)

If the source data contains columns that don’t exist in the target table, those columns are automatically added to the
target_table
 schema. Existing rows receive
NULL
 values for the new columns.

Enable schema evolution in earlier versions
Section titled “Enable schema evolution in earlier versions”

In Delta Lake versions earlier than 4.3, enable schema evolution using one of the following alternatives. Both are also available in Delta Lake 4.3 and above.

Set the
mergeSchema
 option on an individual
write
 or
writeStream
 operation:

  Python

  Scala

(spark.read

.
table
(
"
source_table
"
)

.write

.
option
(
"
mergeSchema
"
,

"
true
"
)

.
mode
(
"
append
"
)

.
saveAsTable
(
"
target_table
"
)
)

spark.read

.table(
"
source_table
"
)

.write

.option(
"
mergeSchema
"
,
"
true
"
)

.mode(
"
append
"
)

.saveAsTable(
"
target_table
"
)

Alternatively, set the Spark configuration
spark.databricks.delta.schema.autoMerge.enabled
 to
true
 to enable schema evolution for all write operations in the current
SparkSession
:

  Python

  Scala

  SQL

spark.conf.
set
(
"
spark.databricks.delta.schema.autoMerge.enabled
"
,

True
)

spark.conf.set(
"
spark.databricks.delta.schema.autoMerge.enabled
"
,
true
)

SET

spark
.
databricks
.
delta
.
schema
.
autoMerge
.
enabled
=
true

When both an operation-level setting (the
mergeSchema
 option or
WITH SCHEMA EVOLUTION
 /
.withSchemaEvolution()
) and the session-wide Spark configuration are specified, the operation-level setting takes precedence.

NullType
 columns
Section titled “NullType columns”

Because Parquet doesn’t support
NullType
,
NullType
 columns are dropped from the DataFrame when writing into Delta tables, but are still stored in the schema. When a different data type is received for that column, Delta Lake merges the schema to the new data type. If Delta Lake receives a
NullType
 for an existing column, the old schema is retained and the new column is dropped during the write.

NullType
 in streaming is not supported. Since you must set schemas when using streaming this should be very rare.
NullType
 is also not accepted for complex types such as
ArrayType
 and
MapType
.

Replace table schema
Section titled “Replace table schema”

By default, overwriting the data in a table does not overwrite the schema. When overwriting a table using mode
overwrite
 without
replaceWhere
, you may still want to overwrite the schema of the data being written. You replace the schema and partitioning of the table by setting the
overwriteSchema
 option to
true
:

  Python

df.write.
option
(
"
overwriteSchema
"
,

"
true
"
)

Views on tables
Section titled “Views on tables”

Delta Lake supports the creation of views on top of Delta tables just like you might with a data source table.

The core challenge when you operate with views is resolving the schemas. If you alter a Delta table schema, you must recreate derivative views to account for any additions to the schema. For instance, if you add a new column to a Delta table, you must make sure that this column is available in the appropriate views built on top of that base table.

Table properties
Section titled “Table properties”

You can store your own metadata as a table property using
TBLPROPERTIES
 in
CREATE
 and
ALTER
. You can then
SHOW
 that metadata. For example:

  SQL

ALTER

TABLE

default
.people10m
SET
 TBLPROPERTIES (
'
department
'

=

'
accounting
'
,
'
delta.appendOnly
'

=

'
true
'
);

-- Show the table's properties.
SHOW TBLPROPERTIES
default
.people10m;

-- Show just the 'department' table property.
SHOW TBLPROPERTIES
default
.people10m (
'
department
'
);

TBLPROPERTIES
 are stored as part of Delta table metadata. You cannot define new
TBLPROPERTIES
 in a
CREATE
 statement if a Delta table already exists in a given location.

In addition, to tailor behavior and performance, Delta Lake supports certain Delta table properties:

Block deletes and updates in a Delta table:
delta.appendOnly=true
.

Configure the
time travel
 retention properties:
delta.logRetentionDuration=<interval-string>
 and
delta.deletedFileRetentionDuration=<interval-string>
. For details, see
Data retention
.

Configure the number of columns for which statistics are collected:
delta.dataSkippingNumIndexedCols=n
. This property indicates to the writer that statistics are to be collected only for the first
n
 columns in the table. Also the data skipping code ignores statistics for any column beyond this column index. This property takes affect only for new data that is written out.

You can also set
delta.
-prefixed properties during the first commit to a Delta table using Spark configurations. For example, to initialize a Delta table with the property
delta.appendOnly=true
, set the Spark configuration
spark.databricks.delta.properties.defaults.appendOnly
 to
true
. For example:

  SQL

  Python

  Scala

spark
.
sql
(
"
SET spark.databricks.delta.properties.defaults.appendOnly = true
"
)

spark.conf.
set
(
"
spark.databricks.delta.properties.defaults.appendOnly
"
,

"
true
"
)

spark.conf.set(
"
spark.databricks.delta.properties.defaults.appendOnly
"
,
"
true
"
)

See also the
Delta table properties reference
.

Syncing table schema and properties to the Hive metastore
Section titled “Syncing table schema and properties to the Hive metastore”

You can enable asynchronous syncing of table schema and properties to the metastore by setting
spark.databricks.delta.catalog.update.enabled
 to
true
. Whenever the Delta client detects that either of these two were changed due to an update, it will sync the changes to the metastore.

The schema is stored in the table properties in HMS. If the schema is small, it will be stored directly under the key
spark.sql.sources.schema
:

  JSON

{

"spark.sql.sources.schema"
:
"
{'name':'col1','type':'string','nullable':true, 'metadata':{}},{'name':'col2','type':'string','nullable':true,'metadata':{}}
"
}

If Schema is large, the schema will be broken down into multiple parts. Appending them together should give the correct schema. For example:

  JSON

{

"spark.sql.sources.schema.numParts"
:
"
4
"
,

"spark.sql.sources.schema.part.1"
:
"
{'name':'col1','type':'string','nullable':tr
"
,

"spark.sql.sources.schema.part.2"
:
"
ue, 'metadata':{}},{'name':'co
"
,

"spark.sql.sources.schema.part.3"
:
"
l2','type':'string','nullable':true,'meta
"
,

"spark.sql.sources.schema.part.4"
:
"
data':{}}
"
}

Table metadata
Section titled “Table metadata”

Delta Lake has rich features for exploring table metadata.

It supports
SHOW COLUMNS
 and
DESCRIBE TABLE
.

It also provides the following unique commands:

DESCRIBE DETAIL
Section titled “DESCRIBE DETAIL”

Provides information about schema, partitioning, table size, and so on. For details, see
Retrieve Delta table details
.

DESCRIBE HISTORY
Section titled “DESCRIBE HISTORY”

Provides provenance information, including the operation, user, and so on, and operation metrics for each write to a table. Table history is retained for 30 days. For details, see
Retrieve Delta table history
.

Configure SparkSession
Section titled “Configure SparkSession”

For many Delta Lake operations, you enable integration with Apache Spark DataSourceV2 and Catalog APIs (since 3.0) by setting the following configurations when you create a new
SparkSession
.

  Python

  Scala

  Java

from
 pyspark.sql
import
 SparkSession

spark
=
 SparkSession \

.builder \

.
appName
(
"
...
"
) \

.
master
(
"
...
"
) \

.
config
(
"
spark.sql.extensions
"
,

"
io.delta.sql.DeltaSparkSessionExtension
"
) \

.
config
(
"
spark.sql.catalog.spark_catalog
"
,

"
org.apache.spark.sql.delta.catalog.DeltaCatalog
"
) \

.
getOrCreate
()

import
 org.apache.spark.sql.
SparkSession

val

spark

=

SparkSession

.builder()

.appName(
"
...
"
)

.master(
"
...
"
)

.config(
"
spark.sql.extensions
"
,
"
io.delta.sql.DeltaSparkSessionExtension
"
)

.config(
"
spark.sql.catalog.spark_catalog
"
,
"
org.apache.spark.sql.delta.catalog.DeltaCatalog
"
)

.getOrCreate()

import

org.apache.spark.sql.SparkSession
;

SparkSession

spark

=

SparkSession

.
builder
()

.
appName
(
"
...
"
)

.
master
(
"
...
"
)

.
config
(
"
spark.sql.extensions
"
,
"
io.delta.sql.DeltaSparkSessionExtension
"
)

.
config
(
"
spark.sql.catalog.spark_catalog
"
,
"
org.apache.spark.sql.delta.catalog.DeltaCatalog
"
)

.
getOrCreate
()
;

Alternatively, you can add configurations when submitting your Spark application using
spark-submit
 or when starting
spark-shell
 or
pyspark
 by specifying them as command-line parameters.

Terminal window
spark-submit

--conf

"
spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension
"

--conf

"
spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog
"

...

Terminal window
pyspark

--conf

"
spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension
"

--conf

"
spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog
"

Configure storage credentials
Section titled “Configure storage credentials”

Delta Lake uses Hadoop FileSystem APIs to access storage systems. The credentials for storage systems usually can be set through Hadoop configurations. Delta Lake provides multiple ways to set Hadoop configurations similar to Apache Spark.

Spark configurations
Section titled “Spark configurations”

When you start a Spark application on a cluster, you can set the Spark configurations in the form of
spark.hadoop.*
 to pass your custom Hadoop configurations. For example, setting a value for
spark.hadoop.a.b.c
 will pass the value as a Hadoop configuration
a.b.c
, and Delta Lake will use it to access Hadoop FileSystem APIs.

See
Spark documentation
 for more details.

SQL session configurations
Section titled “SQL session configurations”

Spark SQL will pass all of the current
SQL session configurations
 to Delta Lake, and Delta Lake will use them to access Hadoop FileSystem APIs. For example,
SET a.b.c=x.y.z
 will tell Delta Lake to pass the value
x.y.z
 as a Hadoop configuration
a.b.c
, and Delta Lake will use it to access Hadoop FileSystem APIs.

DataFrame options
Section titled “DataFrame options”

Besides setting Hadoop file system configurations through the Spark (cluster) configurations or SQL session configurations, Delta supports reading Hadoop file system configurations from
DataFrameReader
 and
DataFrameWriter
 options (that is, option keys that start with the
fs.
 prefix) when the table is read or written, by using
DataFrameReader.load(path)
 or
DataFrameWriter.save(path)
.

For example, you can pass your storage credentials through DataFrame options:

  Python

  Scala

df1
=
 spark.read.
format
(
"
delta
"
) \

.
option
(
"
fs.azure.account.key.<storage-account-name>.dfs.core.windows.net
"
,

"
<storage-account-access-key-1>
"
) \

.
read
(
"
...
"
)
df2
=
 spark.read.
format
(
"
delta
"
) \

.
option
(
"
fs.azure.account.key.<storage-account-name>.dfs.core.windows.net
"
,

"
<storage-account-access-key-2>
"
) \

.
read
(
"
...
"
)
df1.
union
(
df2
).write.
format
(
"
delta
"
) \

.
mode
(
"
overwrite
"
) \

.
option
(
"
fs.azure.account.key.<storage-account-name>.dfs.core.windows.net
"
,

"
<storage-account-access-key-3>
"
) \

.
save
(
"
...
"
)

val

df1

=
 spark.read.format(
"
delta
"
)

.option(
"
fs.azure.account.key.<storage-account-name>.dfs.core.windows.net
"
,
"
<storage-account-access-key-1>
"
)

.read(
"
...
"
)
val

df2

=
 spark.read.format(
"
delta
"
)

.option(
"
fs.azure.account.key.<storage-account-name>.dfs.core.windows.net
"
,
"
<storage-account-access-key-2>
"
)

.read(
"
...
"
)
df1.union(df2).write.format(
"
delta
"
)

.mode(
"
overwrite
"
)

.option(
"
fs.azure.account.key.<storage-account-name>.dfs.core.windows.net
"
,
"
<storage-account-access-key-3>
"
)

.save(
"
...
"
)

You can find the details of the Hadoop file system configurations for your storage in
Storage configuration
.
