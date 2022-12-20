## Linear Regression from Phase 2 with [Spark MLLib](https://spark.apache.org/docs/latest/ml-guide.html)

This code will not run on the standard bitnami Spark image.
- what is the problem?
- how can we fix it?

```python
car_df = spark.read.csv('/data/phase_2/car_data.csv', header=True, inferSchema=True)
car_df.take(1)

car_df.printSchema()

car_df.describe().toPandas().transpose()

import six
for i in car_df.columns:
    if not( isinstance(car_df.select(i).take(1)[0][0], six.string_types)):
        print( "Correlation to selling_price for ", i, car_df.stat.corr('selling_price',i))

from pyspark.ml.feature import VectorAssembler

vectorAssembler = VectorAssembler(inputCols = ['year', 'max_power'], outputCol = 'features')
vcar_df = vectorAssembler.transform(car_df)
vcar_df = vcar_df.select(['features', 'selling_price'])
vcar_df.show(3)

(train_df, test_df) = vcar_df.randomSplit([0.8, 0.4])

from pyspark.ml.regression import LinearRegression

reg = LinearRegression(featuresCol = 'features', labelCol='selling_price', maxIter=10)
reg_model = reg.fit(train_df)

print("Coefficients: " + str(reg_model.coefficients))
print("Intercept: " + str(reg_model.intercept))


reg_predictions = reg_model.transform(test_df)
reg_predictions.select("prediction","selling_price","features").show(5)

from pyspark.ml.evaluation import RegressionEvaluator
reg_evaluator = RegressionEvaluator(predictionCol="prediction", \
                 labelCol="selling_price",metricName="r2")
print("R Squared (R2) on test data = %g" % reg_evaluator.evaluate(reg_predictions))

trainingSummary = reg_model.summary
print("RMSE: %f" % trainingSummary.rootMeanSquaredError)
print("r2: %f" % trainingSummary.r2)
```

