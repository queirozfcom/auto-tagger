
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._
import org.apache.spark.sql.{Column, DataFrame, SaveMode, SparkSession}

import scala.collection.mutable
import org.apache.spark.sql.functions.udf

/**
  * Created by felipe on 04/12/16.
  */
object ReadRawRCV1AndSaveCSV extends App {

  val homeDir = System.getenv("HOME")

  val projectDir = s"file://$homeDir/auto-tagger/data/RawRCV1/"

  val inputDir = s"${projectDir}extracted/"

  val inputFileSingle = s"${projectDir}reuters-full.xml"

  val outputDir = s"${projectDir}csv"

  val outputDirParquet = s"${projectDir}parquet"

  val spark = SparkSession
    .builder()
    .appName("Spark SQL basic example")
    .getOrCreate()

//  spark.sqlContext.setConf("spark.sql.small.file.combine","true")


  //  val customSchema = StructType(Array(
  //    StructField("_itemid", StringType, nullable = true),
  //    StructField("title", StringType, nullable = true),
  //    StructField("text", StringType, nullable = true),
  //    StructField("metadata", StructType(
  //      List(StructField("codes", ArrayType(
  //        StructType(
  //          List(
  //            StructField("_class", StringType, nullable = true),
  //            StructField("code", ArrayType(
  //              StructType(
  //                List(StructField("_code", StringType, nullable = true))
  //              )
  //            ), nullable = true)
  //          )
  //        )),nullable = true)
  //      )), nullable = true)))


  val customSchema = StructType(Array(
    StructField("_itemid", StringType, nullable = true),
    StructField("title", StringType, nullable = true),
    StructField("text", StringType, nullable = true),
    StructField("metadata", StringType, nullable = true)))

  def extractCodes(metadataColumn: String): String = {
    val Pat = """<code code='([^']+)'>""".r
    val matches = Pat.findAllMatchIn(metadataColumn).toList.map(m => m.group(1)).mkString(",")
    matches
  }



//    val dflite = spark.sqlContext.read
//      .format("com.databricks.spark.xml")
//      .schema(customSchema)
//      .option("rowTag", "newsitem")
//      .load(s"$inputDir/104239newsML.xml")




  val extractCodesUdf = udf(extractCodes _)



  println(spark.sqlContext.getAllConfs)

    val df: DataFrame = spark.sqlContext.read
    .format("com.databricks.spark.xml")
    .schema(customSchema)
    .option("rowTag", "newsitem")
    .load(s"$inputFileSingle")
    .repartition(1)

  val dfout = df
    .select(
      df("_itemid").as("id"),
      df("*"),
      extractCodesUdf(df("metadata")).as("tags")
    ).drop("metadata", "_itemid")


  dfout
    .write
    .option("quoteAll", true)
    .mode(SaveMode.Overwrite)
    .csv(outputDir)

}
