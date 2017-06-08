import java.util.Locale

var body:String = "foo bar"

val HTML_TAGS_PATTERN = """<[^>]+>""".r

body = HTML_TAGS_PATTERN.replaceAllIn(body, " ")

"""((?!<=\d)\.(?!\d))""".r.replaceAllIn("foo.bar 5.0  foo5.bar foo5.6bar "," . ")

//"""foo(?!bar)""".r.replaceAllIn("foobar foo","X")

//body.toLowerCase

val input = List(
  """<foobar>adsadsa</foobar>""",
  """<row Id="20553964" PostTypeId="1" AcceptedAnswerId="20553965" CreationDate="2013-12-12T20:50:10.247" Score="8" ViewCount="514" Body="&lt;p&gt;In PyCharm when I move between words with the &lt;code&gt;Alt + ←/→&lt;/code&gt; shortcut it moves the cursor between whitespace separated words. How can I make it move the cursor between &lt;code&gt;underscore_seperated_words&lt;/code&gt;?&lt;/p&gt;&#xA;" OwnerUserId="238166" LastActivityDate="2016-11-27T16:15:00.003" Title="Moving between underscore separated words in PyCharm with Alt + ←/→" Tags="&lt;python&gt;&lt;pycharm&gt;&lt;shortcuts&gt;" AnswerCount="1" CommentCount="0" FavoriteCount="1"><foo bar="quux"></foo></row>"""
)

Locale.getDefault

val parts = input(1).split(""""""")

//var id: String = ""
//var title: String = ""
//var body: String = ""
//var tags: String = ""
//
//parts.zipWithIndex.foreach { case (str, idx) =>
//
//  print(idx, str)
//
//  if (str == "<row Id=") id = parts(idx + 1)
//  if (str == " Body=") body = parts(idx + 1)
//  if (str == " Title=") title = parts(idx + 1)
//  if (str == " Tags=") tags = parts(idx + 1)
//
//
//}
//
//
//id
//title
//body
//tags

val str1 =
  """<p>thanks and regards.</p>

  <pre><code>private void button1_click(object sender, eventargs e)
    {
    button newbutton = new button();
    newbutton.location = new system.drawing.point(0, (y+6));
    buttons.add(newbutton);
    y += 20;
    panel1.controls.add(newbutton);
    }
  </code></pre>","2016-02-14t17:54:20.810"
"8909372","jslint - 'var not defined' errors caused by external script files","<p>i am trying out jslint on some of the javascript file$

<pre><code>js lint: '&lt;var name&gt;' is not defined
</code></pre>

  <p>the issue is that the variable is defined in a separate file that is referenced elsewhere. e.g. the html page has global.js and page$

    <p>i am aware using the syntax</p>

    <pre><code>/* global varname */
    </code></pre>

    <p>to tell jslint that yes infact this variable does exist but this is not ideal in this scenario due to the number of different variab$

      <p>my feeling is that either there is a jslint solution i am unaware of or, perhaps more likely, that is indicative of a problem with h$

        <p>ideas/feedback appreciated.</p>
"""

val htmltagspat = """<[^>]+>""".r

val whitespaceOrNewlinePat = """\s+|\R+""" r

val str2 = htmltagspat.replaceAllIn(str1, " ")

val str3 = whitespaceOrNewlinePat.replaceAllIn(str2, " ")

val tagspat = """<|>"""

val str = "<foo>,<bar>,<baz-quux>"

str.split(tagspat).filterNot(s => s.trim == "" || s.trim == ",").mkString(", ").trim