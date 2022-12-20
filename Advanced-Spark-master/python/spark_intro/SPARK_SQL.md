- load csv file
  ```python
  >>> df = spark.read.option('header', True).csv('/data/python/spark_intro/sample.csv')
  >>> df
  >>> df.show()
  ```

- create a table from the dataframe and query it
  ```python
  >>> df.createTempView('sample')
  >>> spark.sql("SELECT * FROM sample").show()
  >>> spark.sql("SELECT COUNT(1) FROM sample WHERE width > 2 LIMIT 2").show()
  ```
  - what does the `spark.sql` method return?

- create a table from the access log dataset and get top 10 clients by bytes
  ```python
  >>> access_log = spark.read.option('delimiter', ' ').csv('/data/uncommitted/access.log', header=False).withColumnRenamed('_c0', 'client_ip').withColumnRenamed('_c7', 'bytes')
  >>> access_log.createOrReplaceTempView('access_log')
  >>> top_10_clients_by_bytes_template = '''
  SELECT
    client_ip,
    SUM(bytes) total_bytes
  FROM
      {0}
  GROUP BY
      client_ip
  ORDER BY
      total_bytes DESC
  LIMIT 10;
  '''
  ```
- time the query
  ```python
  >>> import time
  >>> start=time.time(); spark.sql(top_10_clients_by_bytes_template.format('access_log')).show(); print(f'csv-backed took {time.time()-start:.2f}s')
  ```

- save the data out in an optimised, columnar format
  ```python
  access_log.write.save('/data/uncommitted/access_log.parquet', format='parquet')
  ```

- load the parquet data and query it as SQL
  ```python
  >>> access_log_parquet = spark.read.load('/data/uncommitted/access_log.parquet')
  >>> access_log_parquet.createOrReplaceTempView('access_log_parquet')
  >>> start=time.time(); spark.sql(top_10_clients_by_bytes_template.format('access_log_parquet')).show(); print(f'parquet-backed took {time.time()-start:.2f}s')

- how much faster is the parquet-backed query? Why?
