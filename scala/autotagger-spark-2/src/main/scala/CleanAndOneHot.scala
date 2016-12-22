import com.queirozf.sparkutils.udfs.splitStringColumnUdf
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._
import org.apache.spark.sql._

import org.apache.spark.ml.feature._

import scala.collection.mutable
import org.apache.spark.sql.functions.udf

import org.apache.spark.mllib.linalg._

/**
  * Created by felipe on 16/12/16.
  */
object CleanAndOneHot extends App {

  val homeDir = System.getenv("HOME")

  val projectDir = s"file://$homeDir/auto-tagger/data/RawRCV1/csv"

  val inputFileSingle = s"${projectDir}/reuters-rcv1-full.csv"

  val outputDir = s"${projectDir}/csv/out"

  val spark = SparkSession
    .builder()
    .appName("Spark SQL basic example")
    .getOrCreate()

  import spark.implicits._

  val schema = StructType(
    Array(
      StructField("id", StringType, nullable = false),
      StructField("title", StringType, nullable = false),
      StructField("text", StringType, nullable = false),
      StructField("tags", StringType, nullable = false)
    )
  )

  case class Document(id: String, title: String, text: String, tagsArray: Array[String])

  val df = spark.read.schema(schema).csv(inputFileSingle)

  val df2 = df.select(df("id"),df("title"),df("text"),splitStringColumnUdf(df("tags")).as("tagsArray")).drop(df("tags"))

  val ds = df2.as[(Array[String], String, String, String)]

  val df3 = ds.toDF()



}
