# Apache Spark

We will run a standalone/local Spark "cluster" in a Docker container and use it to explore the PySpark API.

## Run the Container

`docker run --rm -it -v$(pwd):/data bitnami/spark pyspark`

After a moment you should see a Python prompt.

## Exercises

- Create a list of numbers as an RDD
  ```python
  >>> numbers = sc.parallelize([0,1,2,3,4,5,6,7,8,9])
  >>> numbers
  ParallelCollectionRDD[0] at readRDDFromFile at PythonRDD.scala:274
  ```
  - `numbers` is a Resilient Distributed Dataset, not a Python list
- Print first 5 values
  ```python
  >>> numbers.collect()
  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
  ```
- Double each value
  ```python
  >>> numbers.map(lambda n: n * 2)
  PythonRDD[1] at RDD at PythonRDD.scala:53  
  ```
  - `map` applies a function to every row
  - returns another RDD, not a Python list
  - why does Spark not just print the numbers?
  - how would we print these numbers?
- Filter for multiples of 3
  ```python
  >>> mults_of_3 = numbers.filter(lambda n: n % 3 == 0)
  >>> mults_of_3
  PythonRDD[2] at RDD at PythonRDD.scala:53
  >>> mults_of_3.collect()
  [0, 3, 6, 9]
  ```
  - `filter` selects rows that match the "predicate"
  - what is the predicate in the example?
- Create a string of multiples of 3 in descending order
  ```python
  >>> mults_of_3.sortBy(lambda n: -n).reduce(lambda s, n: str(s) + '|' + str(n))
  '9|6|3|0'
  ```
  - `reduce` works over the RDD, using the function given to combine each value with an "accumulator" value
  
- What do `map`, `filter` and `sortBy` have in common that is different to `collect` and `reduce`?

Note - `map`, `filter` and `reduce` are ideas from "functional programming" - a style of computer programming that lends itself well to distributed computing, so FP terms do come up. This [YouTube video](https://www.youtube.com/watch?v=wVAEOHqC3Cg) is a neat introduction to the idea if you want to know more.

- Read a file
  ```python
  >>> text = sc.textFile('README.md')
  >>> text.count()
  108
  >>> text.foreach(print)

    ./bin/pyspark

  And run the following command, which should also return 1,000,000,000:
  ...
  ```
  - where is the `README.md` file we are reading?
  - how would we read the `Dockerfile` file in the root of this repo?
  - how many lines mention './bin'?
  - what is the mean line length?

- Can you calculate the number of lines of each length in the file?

- Write results (you'll need to allow write access to all in `uncommitted` for this to work: `chmod 777 uncommitted` in the root of the project)
  ```python
  >>> import time
  >>> text = sc.textFile('README.md').filter(lambda line: 'Spark' in line).saveAsTextFile(f'/data/uncommitted/spark_lines_{time.time()}')
  ```
  - we template in a timestamp to avoid permissions issues when trying to run the code again
  - `sudo rm -rf uncommitted/spark_lines*` to delete the output produced by the container
