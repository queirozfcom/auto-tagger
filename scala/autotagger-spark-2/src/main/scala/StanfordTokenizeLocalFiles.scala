import java.io.{FileReader, FileWriter}

import au.com.bytecode.opencsv.{CSVReader, CSVWriter}

import scala.io.Source

import ReadSOStanfordTokenize.Helpers.tokenizePost

/**
  * Created by felipe on 12/06/17.
  */
object StanfordTokenizeLocalFiles extends App{

  val input = "/media/felipe/SAMSUNG/StackHeavy/Posts-shuffled/Small-Sample-Posts-Shuffled.csv"

  val output = input.replace("Small-Sample-Posts-Shuffled.csv","Small-Sample-Posts-Shuffled-Stanford-Tokenized.csv")

  val bufferedSource = Source.fromFile(input)

  val reader = new CSVReader(new FileReader(input))

  val writer = new CSVWriter(new FileWriter(output),CSVWriter.DEFAULT_SEPARATOR,CSVWriter.DEFAULT_QUOTE_CHARACTER,'\\')

  var nextLine: Seq[String] = reader.readNext()

  do {

    val Seq(id,title,body,tags) = nextLine

    writer.writeNext(Array(id,tokenizePost(title,body,unescapeXml = true),tags))

    nextLine = reader.readNext()

  } while (nextLine != null)

  // need this otherwise the writer may not write everything to the file
  // by the time the loop ends
  writer.flush()

}
