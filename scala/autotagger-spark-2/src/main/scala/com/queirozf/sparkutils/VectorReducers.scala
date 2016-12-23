package com.queirozf.sparkutils

import org.apache.spark.ml.linalg._

object VectorReducers {

  def or(vec1: Vector, vec2: Vector): Vector = {

    assert(vec1.size == vec2.size, "Can only combine vectors of the same length!!!")

    val sp1 = vec1.toSparse
    val sp2 = vec2.toSparse

    val indices = (sp1.indices ++ sp2.indices).distinct.sorted

    val out: Array[(Int, Double)] = indices.map { idx =>
      if (sp1(idx) == 1.0 || sp2(idx) == 1.0) (idx, 1.0) else (idx, 0.0)
    }

    // i know it's stupid to traverse the thing twice but I was getting weird errors
    // on spark-shell
    val outIndices = out.map(_._1)
    val outValues = out.map(_._2)

    new SparseVector(sp1.size, outIndices, outValues)

  }

}