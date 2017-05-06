import com.queirozf.sparkutils.VectorReducers
import com.queirozf.sparkutils.udfs.splitStringColumnUdf
import com.queirozf.sparkutils.udfs.mkStringUdf
import org.apache.spark.ml.feature._
import org.apache.spark.ml.linalg._
import org.apache.spark.rdd.RDD
import org.apache.spark.sql._
import org.apache.spark.sql.types._
import org.apache.spark.sql.functions.udf
import com.queirozf.sparkutils.udfs.splitStringColumnUdf
import org.apache.spark.sql.functions.rand

/**
  * Created by felipe on 27/04/17.
  */
object ReadSOXMLShuffleAndSaveCSV extends App {

  // reads an xml file containing posts, selects only questions (type ==1)
  // using spark-xml


  val SEED = 42

  val pathToInputXML = args(0)

  val numPartitions = args(1).toInt

  //  val outNumPartitions = args(2).toInt

  val output = pathToInputXML.replace(".xml", "-csv")

  //  val output = "/home/felipe/spark-output"

  val spark = SparkSession
    .builder()
    .appName("Spark SQL basic example")
    .getOrCreate()

  import spark.implicits._

  val customSchema = StructType(Array(
    StructField("_Id", StringType, nullable = true),
    StructField("_Title", StringType, nullable = true),
    StructField("_PostTypeId", StringType, nullable = true),
    StructField("_Body", StringType, nullable = true),
    StructField("_Tags", StringType, nullable = true)))

  case class Post(id: String, title: String, body: String, tags: String)

  case class Post2(id: String, title: String, body: String, tags: Array[String])


  val df: DataFrame = spark.sqlContext.read
    .option("mode", "DROPMALFORMED")
    .format("com.databricks.spark.xml")
    .schema(customSchema)
    .option("rowTag", "row")
    .load(s"$pathToInputXML")
    .repartition(numPartitions)

  println(s"\n\nNUM PARTITIONS: ${df.rdd.getNumPartitions}\n\n")

  df
    .where(df.col("_PostTypeId") === "1")
    .select(
      df("_Id").as("id"),
      df("_Title").as("title"),
      df("_Body").as("body"),
      df("_Tags").as("tags")
    ).as[Post]
    .map {
      case Post(id, title, body, tags) =>
        Post(id, title.toLowerCase, body.toLowerCase, tags.toLowerCase)
    }
    .orderBy(rand(SEED))
    .foreachPartition { rdd =>
      if (rdd.nonEmpty) {
        println(s"HI! I'm an RDD and I have ${rdd.size} elements!")
      }
    }
  //    .write
  //    .option("quoteAll", true)
  //    .mode(SaveMode.Overwrite)
  //    .csv(output)

}
