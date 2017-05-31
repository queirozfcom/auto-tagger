import org.apache.spark.sql.SQLContext
import org.apache.spark.sql.types.{StructType, StructField, StringType, IntegerType}
import org.apache.spark.sql.Row
import org.apache.spark.ml.feature._
import org.apache.spark.sql.types.{StructType, StructField, StringType, IntegerType}
import org.apache.spark.{SparkContext, SparkConf}
import org.apache.spark.sql.functions.udf

// this example was written for spark 1.6.x and has not yet been converted to spark 2.x format.
// it might work, but it may not.
object Word2Vec  {

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
    val removeHtmlTags = udf { str: String =>
      val tagsPat = """<[^>]+>""".r
      tagsPat.replaceAllIn(str, "")
    }

    val df1 = df
      .withColumn("cleanBody", removeHtmlTags(df("body")))
      .drop(df("body"))

    val df2 = new Tokenizer()
      .setInputCol("cleanBody")
      .setOutputCol("bodyTokens")
      .transform(df1)
      .drop(df1("cleanBody"))

    val word2Vec = new Word2Vec()
      .setInputCol("bodyTokens")
      .setOutputCol("vectors")
      .setVectorSize(50)
      .setMinCount(10)

    val df3 = word2Vec.fit(df2).transform(df2)

    println("--------------")
    println("--------------")
    println("--------------")
    println("--------------")
    df3.show()



  }

}
