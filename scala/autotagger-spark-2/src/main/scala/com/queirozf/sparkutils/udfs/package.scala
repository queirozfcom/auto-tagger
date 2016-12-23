package com.queirozf.sparkutils

import org.apache.spark.sql.expressions.UserDefinedFunction
import org.apache.spark.sql.functions._

import scala.collection.JavaConverters._

/**
  * Created by felipe on 16/12/16.
  */
package object udfs {

  def extractCodes(metadataColumn: String): String = {
    val Pat = """<code code='([^']+)'>""".r
    val matches = Pat.findAllMatchIn(metadataColumn).toList.map(m => m.group(1)).mkString(",")
    matches
  }

  def splitStringColumn(str: String) : Array[String] = {
    if(str == null) Array.empty[String]
    else str.split(",")
  }

  val splitStringColumnUdf: UserDefinedFunction = udf(splitStringColumn _)

  val extratCodesUdf: UserDefinedFunction = udf(extractCodes _)


}
