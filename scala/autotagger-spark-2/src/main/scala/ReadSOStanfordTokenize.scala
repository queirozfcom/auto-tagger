import java.io.StringReader

import edu.stanford.nlp.ling.CoreLabel
import edu.stanford.nlp.process.{CoreLabelTokenFactory, PTBTokenizer}
import org.apache.commons.lang3.StringEscapeUtils
import org.apache.spark.sql._

/**
  * Created by felipe on 27/04/17.
  */
object ReadSOStanfordTokenize extends App {

  // reads an xml file containing posts, selects only questions (type ==1)
  // using regular sc.TextFile because spark-xml crashes evrything
  // see https://stackoverflow.com/questions/43796443/out-of-memory-error-when-reading-large-file-in-spark-2-1-0


  val pathToInputFile = args(0)

  val numPartitions = args(1).toInt

  val pathToOutputFile = pathToInputFile.replace(".xml", ".txt")

  val spark = SparkSession
    .builder()
    .appName("Spark SQL basic example")
    .getOrCreate()


  case class Post(title: String, body: String)

  import java.util.Locale

  import spark.implicits._

  Locale.setDefault(new Locale("en", "US"))

  spark
    .sparkContext
    .textFile(pathToInputFile, numPartitions)
    .filter { str => str.startsWith("  <row ") }
    .toDS()
    .map { str =>

      val HTML_TAGS_PATTERN = """<[^>]+>"""
      val WHITESPACE_OR_NEWLINE_PATTERN = """\s+|\R+"""
      val FORWARD_SLASH_PATTERN = """((?<!\d)/(?!\d))""" // slash not preceded a digit, not followed by a digit
      val DOT_PATTERN = """((?!<=\d)\.(?!\d))""" // dot not preceded by a digit, not followed by a digit

      val OPTIONS = "ptb3Escaping=false"

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
      if(title.endsWith("?") || title.endsWith(".") || title.endsWith(".")){
        // do nothing
      }else{
        title = title + "." // to signal the end of the sentence.
      }

      body = StringEscapeUtils.unescapeXml(body).toLowerCase // decode xml entities
      body = HTML_TAGS_PATTERN.r.replaceAllIn(body, " ") // take out htmltags
      body = FORWARD_SLASH_PATTERN.r.replaceAllIn(body," / ") // otherwise the tokenizer doesn't consider a "/" as a delimiter
      body = DOT_PATTERN.r.replaceAllIn(body," . ") // to make all dots be delimiters, not just some (except in numbers)
      body = WHITESPACE_OR_NEWLINE_PATTERN.r.replaceAllIn(body, " ") // replace multiple whitespaces/newlines with a single one

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

      // after tokenizing, remove spaces between triple dots

      out = """\.\s\.\s\.""".r.replaceAllIn(out," ... ")
      out = WHITESPACE_OR_NEWLINE_PATTERN.r.replaceAllIn(out, " ") // again, because of the above

      out.trim

    }
    .write
    .mode(SaveMode.Overwrite)
    .text(pathToOutputFile)

}
