
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._
import org.apache.spark.sql.{DataFrame, SparkSession}


/**
  * Created by felipe on 04/12/16.
  */
object ReadRawRCV1 extends App {

  val homeDir = System.getenv("HOME")

  val inputDir = s"file://$homeDir/auto-tagger/data/RawRCV1/extracted/"

  val spark = SparkSession
    .builder()
    .appName("Spark SQL basic example")
    .getOrCreate()

  val customSchema = StructType(Array(
    StructField("_itemid", StringType, nullable = true),
    StructField("title", StringType, nullable = true),
    StructField("text", StringType, nullable = true),
    StructField("metadata", StructType(
      List(StructField("codes", ArrayType(
        StructType(
          List(
            StructField("_class", StringType, nullable = true),
            StructField("code", ArrayType(
              StructType(
                List(StructField("_code", StringType, nullable = true))
              )
            ), nullable = true)
          )
        )),nullable = true)
      )), nullable = true)))

  import spark.implicits._

  val df: DataFrame = spark.sqlContext.read
    .format("com.databricks.spark.xml")
    .schema(customSchema)
    .option("rowTag", "newsitem")
    .load(s"$inputDir/*")


  df.printSchema()

  df.show(10)

}
