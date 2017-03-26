import com.queirozf.sparkutils.VectorReducers
import com.queirozf.sparkutils.udfs.splitStringColumnUdf
import com.queirozf.sparkutils.udfs.mkStringUdf
import org.apache.spark.ml.feature._
import org.apache.spark.ml.linalg._
import org.apache.spark.rdd.RDD
import org.apache.spark.sql._
import org.apache.spark.sql.types._

import scala.collection.mutable

/**
  * Created by felipe on 09/01/17.
  */
object ReadCSVAndTokenizeDocuments extends App {

  val homeDir = System.getenv("HOME")

  val projectDir = s"file://$homeDir/auto-tagger/data/rcv1"

  val fullInputFileSingle = s"${projectDir}/csv/in/reuters-rcv1-full.csv"

  val sampleInputFileSingle = s"${projectDir}/csv/in/xaa"

  val outputPath = s"${projectDir}/string/out"

  val spark = SparkSession
    .builder()
    .appName("Spark SQL basic example")
    .getOrCreate()

  val schema = StructType(
    Array(
      StructField("id", StringType, nullable = false),
      StructField("title", StringType, nullable = false),
      StructField("text", StringType, nullable = false),
      StructField("tags", StringType, nullable = false)
    )
  )

  import spark.implicits._

  case class Document(id: String, title: String, text: String, tags: String)

  val ds = spark.read
    .option("mode", "DROPMALFORMED")
    .option("escape","""\""")
    .schema(schema)
    .csv(fullInputFileSingle)
    .as[Document]
    .filter( d => d.text != null)


  val clean = ds.map {
    case d: Document => {
      d.text
        .toLowerCase
        .replaceAll("""<[^>]{1,10}>""", " ")

    }
  }.toDF("text")


  val regexTokenizer = new RegexTokenizer()
    .setInputCol("text")
    .setOutputCol("words")
    .setPattern("""\W+""")
    .setMinTokenLength(2)
    .setGaps(true)


  val tokenizedDf = regexTokenizer.transform(clean).drop("text")

  val mergedDf: DataFrame = tokenizedDf.select(mkStringUdf(tokenizedDf.col("words")).as("textString"))

  mergedDf
    .repartition(10)
    .write
    .mode(SaveMode.Overwrite)
    .text(outputPath)

}
