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
import org.apache.spark.sql.functions.rand
import java.io.StringReader
import java.util.Locale

import ReadCSVAndTokenizeDocuments.outputPath
import edu.stanford.nlp.process.PTBTokenizer
import edu.stanford.nlp.ling.CoreLabel
import edu.stanford.nlp.process.CoreLabelTokenFactory

/**
  * Created by felipe on 27/04/17.
  */
object ReadSOStanfordTokenize extends App {

  // reads an xml file containing posts, selects only questions (type ==1)
  // using regular sc.TextFile because spark-xml crashes evrything
  // see https://stackoverflow.com/questions/43796443/out-of-memory-error-when-reading-large-file-in-spark-2-1-0


  val SEED = 42

  val rng = scala.util.Random

  rng.setSeed(SEED)

  val pathToInputFile = args(0)

  val numPartitions = args(1).toInt

  //  val outNumPartitions = args(2).toInt

  val pathToOutputFile = pathToInputFile.replace(".xml", ".txt")


  //  val OPTIONS = "ptb3Escaping=false,asciiQuotes=true"
  val OPTIONS = "ptb3Escaping=false"

  val spark = SparkSession
    .builder()
    .appName("Spark SQL basic example")
    .getOrCreate()


  case class Post(title: String, body: String)

  import spark.implicits._

  val HTML_TAGS_PATTERN = """<[^>]+>"""

  val WHITESPACE_OR_NEWLINE_PATTERN = """\s+|\R+"""

  import java.util.Locale

  Locale.setDefault(new Locale("en", "US"))

  spark
    .sparkContext
    .textFile(pathToInputFile, numPartitions)
    .filter { str => str.startsWith("  <row ") }
    .toDS()
    .map { str =>

      Locale.setDefault(new Locale("en", "US"))

      val parts = str.split(""""""")

      val locale = Locale.getDefault

      println("locale is: " + locale.getDisplayName)

      var title: String = ""
      var body: String = ""

      // these fields sometimes come out of order so we can't just say that part(3) is always field "title"
      // also, only  questions have titles, answers only have body
      parts.zipWithIndex.foreach { case (s, idx) =>

        if (s.trim == "Body=") body = parts(idx + 1)
        if (s.trim == "Title=") title = parts(idx + 1)

      }

      title = StringEscapeUtils.unescapeXml(title).toLowerCase.trim
      body = StringEscapeUtils.unescapeXml(body).toLowerCase // decode xml entities

      body = """<[^>]+>""".r.replaceAllIn(body, " ") // take out htmltags
      body = """\s+|\R+""".r.replaceAllIn(body, " ").trim // replace multiple whitespaces with a single one


      val rawText = title + " " + body

      val tok = new PTBTokenizer[CoreLabel](
        new StringReader(rawText),
        new CoreLabelTokenFactory(),
        OPTIONS)

      var out: String = ""

      while (tok.hasNext) {
        val next = tok.next()
        out += next + " "
      }

      out.trim

    }
    .write
    .mode(SaveMode.Overwrite)
    .text(pathToOutputFile)

}
