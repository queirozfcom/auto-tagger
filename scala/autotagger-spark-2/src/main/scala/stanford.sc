import java.io.StringReader

import edu.stanford.nlp.process.PTBTokenizer
import edu.stanford.nlp.ling.CoreLabel
import edu.stanford.nlp.process.CoreLabelTokenFactory


val txt = "i      am using zend form to create a form. i am also using mootools for javascript. $this-&gt;addelement('radio', 'alone', array( 'label' =&gt; 'are you going to be taking part with anyone else?', 'required' =&gt; true, 'onclick' =&gt; 'showfields();', 'multioptions' =&gt; array( 'yes' =&gt; 'yes', 'no' =&gt; 'no' )) ); at the moment, the onclick event works if any option is selected. how do i get it to work for just yes being selected?"

val options = "ptb3Escaping=false,asciiQuotes=true"

val tok = new PTBTokenizer[CoreLabel](
  new StringReader(txt),
  new CoreLabelTokenFactory(),
  options)

while (tok.hasNext){
  val label = tok.next()
  print(label+" ")
}
