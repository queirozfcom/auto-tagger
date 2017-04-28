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

/**
  * Created by felipe on 27/04/17.
  */
object ReadSOXMLAndSaveCSV extends App {

  val pathToInputXML = args(0)

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

  case class Post(id:String, title: String, body: String, tags: String)
  case class Post2(id:String, title: String, body: String, tags: Array[String])

//  println(spark.sqlContext.getAllConfs)

  val df: DataFrame = spark.sqlContext.read
    .option("mode", "DROPMALFORMED")
    .format("com.databricks.spark.xml")
    .schema(customSchema)
    .option("rowTag", "row")
    .load(s"$pathToInputXML")
    .repartition(200)

  val dsout = df
    .where( df.col("_PostTypeId") === "1" )
    .select(
      df("_Id").as("id"),
      df("_Title").as("title"),
      df("_Body").as("body"),
      df("_Tags").as("tags")
    ).as[Post]

  val tagPat = "<[^>]+>".r

  val angularBracketsPat = "><|>|<"

  val whitespacePat = """\s+""".r

  dsout
    .map{
      case Post(id,title,body,tags) =>

        val body1 = tagPat.replaceAllIn(body,"")
        val body2 = whitespacePat.replaceAllIn(body1," ")

        Post(id,title.toLowerCase,body2.toLowerCase, tags.split(angularBracketsPat).mkString(","))

    }
    .write
    .option("quoteAll", true)
    .mode(SaveMode.Overwrite)
    .csv(output)

}
