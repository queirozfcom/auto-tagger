package com.queirozf.sparkutils

import org.apache.spark.sql.expressions.UserDefinedFunction
import org.apache.spark.sql.functions._

import scala.collection.JavaConverters._
import scala.collection.mutable

/**
  * Created by felipe on 16/12/16.
  */
package object udfs {

  def extractCodes(metadataColumn: String): String = {
    val Pat = """<code code='([^']+)'>""".r
    val matches = Pat.findAllMatchIn(metadataColumn).toList.map(m => m.group(1)).mkString(",")
    matches
  }

  def splitStringColumn(str: String): Array[String] = {
    if (str == null) Array.empty[String]
    else str.split(",")
  }

  def mkString(arr: mutable.WrappedArray[String]): String = {
    if(arr == null ) " "
    else arr.mkString(" ")
  }

  val splitStringColumnUdf: UserDefinedFunction = udf(splitStringColumn _)

  val extratCodesUdf: UserDefinedFunction = udf(extractCodes _)

  val mkStringUdf: UserDefinedFunction = udf(mkString _)

}
