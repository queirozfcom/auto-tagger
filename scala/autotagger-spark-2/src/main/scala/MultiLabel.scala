import org.apache.spark.mllib.linalg.DenseVector
import org.apache.spark.sql.SQLContext
import org.apache.spark.sql.types.{StructType, StructField, StringType, IntegerType}
import org.apache.spark.sql.Row
import org.apache.spark.ml.feature._
import org.apache.spark.sql.types.{StructType, StructField, StringType, IntegerType}
import org.apache.spark.{SparkContext, SparkConf}
import org.apache.spark.sql.functions.udf
import org.apache.spark.ml.classification.{NaiveBayes, OneVsRest, LogisticRegression}



// this example was written for spark 1.6.x and has not yet been converted to spark 2.x format.
// it might work, but it may not.
object MultiLabel {

  def main(args: Array[String]) {

    val cnf = new SparkConf().setAppName("Auto-tagger word2vec")

    val sc = new SparkContext(cnf)

    val sqlContext = new SQLContext(sc)

    val schema = StructType(Array(
      StructField("id", StringType, true),
      StructField("title", StringType, true),
      StructField("body", StringType, true),
      StructField("tags", StringType, true)))

    val df = sqlContext.read
      .format("com.databricks.spark.csv")
      .option("mode", "DROPMALFORMED")
      .schema(schema)
      .load("/home/felipe/auto-tagger/data/stackoverflow/pieces/aa")

    val count = df.count()

    // no html tags
    val removeHtmlTagsUDF = udf { str: String =>
      val tagsPat = """<[^>]+>""".r
      tagsPat.replaceAllIn(str, "")
    }

    val df1 = df
      .withColumn("cleanBody", removeHtmlTagsUDF(df("body")))
      .drop(df("body"))

    val splitOnSpaceUDF = udf { str: String =>
      str.split(" ")
    }

    val df2 = df1
      .withColumn("tags-array", splitOnSpaceUDF(df1("tags")))
      .drop(df1("tags"))

    //    val toLinalgVectorUDF = udf{ arr:Array[String] =>
    //      new DenseVector()
    //    }

    val indexer = new VectorIndexer()
      .setInputCol("tags-array")
      .setOutputCol("tags-indexes")
      .fit(df2)


    val base = new LogisticRegression()

    val ovr = new OneVsRest()
    ovr.setClassifier(base)
    val  ovrModel = ovr.fit(df2)


    //    val encoder = new OneHotEncoder()
    //      .setInputCol("tags-array")
    //      .setOutputCol("tags")
    //
    //    val df3 = encoder.transform(df2)


  }

}
