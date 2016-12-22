import com.queirozf.sparkutils.udfs.splitStringColumnUdf
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._
import org.apache.spark.sql._
import org.apache.spark.ml.feature._
import org.apache.spark.sql.expressions.UserDefinedFunction

import scala.collection.mutable
import org.apache.spark.sql.functions.udf
import org.apache.spark.mllib.linalg._
import org.apache.spark.rdd.RDD

/**
  * Created by felipe on 16/12/16.
  */
object CleanAndOneHot extends App {

  val homeDir = System.getenv("HOME")

  val projectDir = s"file://$homeDir/auto-tagger/data/RawRCV1/csv"

  //  val inputFileSingle = s"${projectDir}/reuters-rcv1-full.csv"

  val inputFileSingle = s"${projectDir}/xaa"

  val outputDir = s"${projectDir}/csv/out"

  val spark = SparkSession
    .builder()
    .appName("Spark SQL basic example")
    .getOrCreate()

  import spark.implicits._

  val schemaMultiLabel = StructType(
    Array(
      StructField("id", StringType, nullable = false),
      StructField("title", StringType, nullable = false),
      StructField("text", StringType, nullable = false),
      StructField("tags", StringType, nullable = false)
    )
  )

  val schemaSingleLabel = StructType(
    Array(
      StructField("id", StringType, nullable = false),
      StructField("title", StringType, nullable = false),
      StructField("text", StringType, nullable = false),
      StructField("tag", StringType, nullable = false)
    )
  )

  case class Document(id: String, title: String, text: String, tagsArray: Array[String])


  val df: DataFrame = spark.read.schema(schemaMultiLabel).csv(inputFileSingle)

  val df2 = df.select(df("id"), df("title"), df("text"), splitStringColumnUdf(df("tags")).as("tagsArray")).drop(df("tags"))

  val ds: Dataset[Document] = df2.as[Document]

  val singleLabelRdd: RDD[Row] = df2.rdd.flatMap { case Row(id: String, title: String, text: String, tagsArray: mutable.WrappedArray[_]) =>
    tagsArray.map(aTag => Row(id, title, text, aTag))
  }

  val singleLabelDF: DataFrame = spark.createDataFrame(singleLabelRdd, schemaSingleLabel)

  // one hot encoding
  val indexer = new StringIndexer().setInputCol("tag").setOutputCol("tagIndex")

  val indexed = indexer.fit(singleLabelDF).transform(singleLabelDF).drop("tag")

  val encoder = new OneHotEncoder().setInputCol("tagIndex").setOutputCol("tagVector")

  val encoded = encoder.transform(indexed).drop("tagIndex")

  

  //  val ds = df2.as[(Array[String], String, String, String)]


  // works lazily but errors if I call count() or any other action
  //  ds.flatMap{ case Document(id,title,text,tags) => tags.map(t => (id,title,text,t))}

  //  val df3 = ds.toDF()


}
