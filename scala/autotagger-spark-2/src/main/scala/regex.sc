

val input = """<foobar>adsadsa</foobar>"""

val pat = "<[^>]+>".r

pat.replaceAllIn(input,"")

val arr = Array.empty[String]

arr.mkString(" ")
