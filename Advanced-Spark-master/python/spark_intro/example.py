from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('TDA_Spark_Intro').getOrCreate()

readme = spark.sparkContext.textFile('README.md')

total_line_length = readme.filter(lambda line: line != '').map(len).sum()

print(f'tll: {total_line_length}')
