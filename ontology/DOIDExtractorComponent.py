import progressbar
from pronto import Ontology
import spacy
from spacy import displacy
from spacy.tokens import Doc, Span, Token
from spacy.lang.en import English
from spacy.matcher import PhraseMatcher
from spacy.util import filter_spans
from spacy.language import Language

@Language.factory("doid_extractor")
class DOIDExtractorComponent(object):
    
    # name of the component
    name = "doid_extractor"
    
    def __init__(self, nlp, name, label="DOID"):
        # label that is applied to the matches
        self.label = label

        # load ontology
        print("Loading DOID ontology")
        doid = Ontology("http://purl.obolibrary.org/obo/doid.obo")
        
        # init terms and patterns
        self.terms = {}
        patterns = []

        i = 0
        nr_terms = len(doid.terms())
        # init progress bar as loading terms takes long
        print("Importing terms")
        bar = progressbar.ProgressBar(maxval=nr_terms, 
                                      widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()

        # iterate over terms in ontology
        for term in doid.terms():
          # if term has a name
          if term.name is not None:
            self.terms[term.name.lower()] = {'id': term.id}
            patterns.append(nlp(term.name))
          i += 1
          bar.update(i)
            
        bar.finish()
        
        # initialize matcher and add patterns
        self.matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
        self.matcher.add(label, None, *patterns)
        
        # set extensions to tokens, spans and docs
        Token.set_extension("is_doid_term", default=False, force=True)
        Token.set_extension("doid_id", default=False, force=True)
        Token.set_extension("merged_concept", default=False, force=True)
        Doc.set_extension("has_doids", getter=self.has_doids, force=True)
        Doc.set_extension("doids", default=[], force=True)
        Span.set_extension("has_doids", getter=self.has_doids, force=True)
        
    def __call__(self, doc):
        matches = self.matcher(doc)
        spans = [Span(doc, match[1], match[2], label=self.label) for match in matches]
        for i, span in enumerate(spans):
          span._.set("has_doids", True)
          for token in span:
               token._.set("is_doid_term", True)
               token._.set("doid_id", self.terms[span.text.lower()]["id"])

        with doc.retokenize() as retokenizer:
            for span in filter_spans(spans):
                retokenizer.merge(span, attrs={"_": {"merged_concept": True}})
                doc._.doids = list(doc._.doids) + [span]

        return doc
    # setter function for doc level
    def has_doids(self, tokens):
        return any([t._.get("is_doid_term") for t in tokens])


# python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")

# doid_extractor = DOIDExtractorComponent(nlp)
nlp.add_pipe("doid_extractor",config={"label": "DOID"})

# Random sample sentences from the publication:
# "Pulmonary and Cardiac Pathology in Covid-19: The First Autopsy Series from New Orleans", Sharon E. Fox et.al.
test = """
Whether this may represent an early manifestation of a viral myocarditis is not certain,
but there was no significant brisk lymphocytic inflammatory infiltrate consistent with the
typical pattern of viral myocarditis...
There is prior evidence of viral infection causing activation of both maladaptive cytokine pathways,
and platelet response, and our findings suggest that these immune functions may be related to
severe forms of Covid-19. In response to systemic and pulmonary viral infections of H1N1
influenza and dengue, megakaryocytes have been known to respond by overexpressing IFITM3,
and producing platelets with the same over-expression.
"""
doc = nlp(test)

# print DOIDs identified
for token in doc:
    if token._.is_doid_term:
        print("http://purl.obolibrary.org/obo/{}\t\t{}".format(token._.doid_id.replace(":","_"), token.text))

# Output: 
# http://purl.obolibrary.org/obo/DOID_820         myocarditis
# http://purl.obolibrary.org/obo/DOID_820         myocarditis
# http://purl.obolibrary.org/obo/DOID_0080600     Covid-19
# http://purl.obolibrary.org/obo/DOID_8469        influenza
