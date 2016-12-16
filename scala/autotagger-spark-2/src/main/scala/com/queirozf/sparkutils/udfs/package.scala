package com.queirozf.sparkutils

import org.apache.spark.sql.expressions.UserDefinedFunction
import org.apache.spark.sql.functions._

/**
  * Created by felipe on 16/12/16.
  */
package object udfs {

  private def extractCodes(metadataColumn: String): String = {
    val Pat = """<code code='([^']+)'>""".r
    val matches = Pat.findAllMatchIn(metadataColumn).toList.map(m => m.group(1)).mkString(",")
    matches
  }

  val splitStringColumnUdf = udf { input: String => input.split(",") }

  val extratCodesUdf: UserDefinedFunction = udf(extractCodes _)


}
