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

import org.apache.commons.lang3.StringEscapeUtils

/**
  * Created by felipe on 27/04/17.
  */
object ReadSOShuffleAndSaveCSV extends App {

  // reads an xml file containing posts, selects only questions (type ==1)
  // using regular sc.TextFile because spark-xml crashes evrything
  // see https://stackoverflow.com/questions/43796443/out-of-memory-error-when-reading-large-file-in-spark-2-1-0


  val SEED = 42

  val rng = scala.util.Random
  rng.setSeed(SEED)

  val pathToInputFile = args(0)

  val numPartitions = args(1).toInt

  val outNumPartitions = args(2).toInt

  val output = pathToInputFile.replace(".xml", "-shuffled")

  val spark = SparkSession
    .builder()
    .appName("Spark SQL basic example")
    .getOrCreate()


  case class Post(id: String, title: String, body: String, tags: String)

  import spark.implicits._

  val rdd = spark.sparkContext.textFile(pathToInputFile, numPartitions)

  val htmlTagsPat = """<[^>]+>""".r

  val whitespaceOrNewlinePat = """\s+|\R+""".r

  val tagspat = """<|>"""

  rdd
    .filter { str => str.startsWith("  <row ") && str.contains("""PostTypeId="1"""") }
    .sortBy(_ => rng.nextInt(), numPartitions = outNumPartitions)
    .toDS()
    .map { str =>

      val parts = str.split(""""""")

      var id: String = ""
      var title: String = ""
      var body: String = ""
      var tags: String = ""

      // these fields sometimes come out of order so we can't just say that part(3) is always field "title"
      parts.zipWithIndex.foreach { case (s, idx) =>

        if (s.trim == "<row Id=") id = parts(idx + 1)
        if (s.trim == "Body=") body = parts(idx + 1)
        if (s.trim == "Title=") title = parts(idx + 1)
        if (s.trim == "Tags=") tags = parts(idx + 1)

      }

      id = id.trim

      title = StringEscapeUtils.unescapeXml(title).toLowerCase.trim

      body = StringEscapeUtils.unescapeXml(body).toLowerCase
      body = htmlTagsPat.replaceAllIn(body, " ")
      body = whitespaceOrNewlinePat.replaceAllIn(body, " ").trim

      tags = StringEscapeUtils.unescapeXml(tags).toLowerCase
      // TODO FIXME
      tags = tags.split(tagspat).filterNot(s => s.trim == "" || s.trim == ",").mkString(", ").trim

      Post(
        id,
        title,
        body,
        tags
      )

    }
    .toDF()
    .write
    .option("quoteAll", true)
    .mode(SaveMode.Overwrite)
    .csv(output)

}
