import ReadSOStanfordTokenize.Helpers


val title1 = """replacing asp datagrid control to custom jquery control (telerik, or other library)"""
val body1 = "i'm creating an app that will create a section associated the orgunitid created by the user. i'm using c#. however, the code below does not work. when i debugged it, the number of attempts is 0. what should i do to send a request and create a new section properly? private void apicreatesection(string host, id2lusercontext usercontext) { string orgunitid = textboxorgunitid.text; string sectioncreateroute = \"/d2l/api/lp/1.0/\" + orgunitid + \"/sections/\"; var client = new restclient(host); var valenceauthenticator = new d2l.extensibility.authsdk.restsharp.valenceauthenticator(usercontext); var requestcreatesection = new restrequest(sectioncreateroute, method.post); requestcreatesection.addjsonbody(new { name = \"section test1\", code = \"123123\", description = new { content = \"description\", type = \"html\" } }); valenceauthenticator.authenticate(client, requestcreatesection); }"



print(Helpers.tokenizePost("","paragraph/starting"))

