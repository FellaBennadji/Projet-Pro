from errant.alignment import Alignment
from spacy.tokens import Doc

# Main module
class Annotator:


    # Input 2: A spacy processing object for the language
    # Input 3: A merging module for the language
    # Input 4: A classifier module for the language
    def __init__(self, nlp=None, merger=None, classifier=None):
        self.nlp = nlp
        self.merger = merger
        self.classifier = classifier

    # Input 1: A text string
    # Input 2: A flag for word tokenisation
    # Output: The input string parsed and tokenized by spacy
    def tag(self, text, tokenise=True):
        if tokenise:
            text = self.nlp(text)
        else:
            text = Doc(self.nlp.vocab, text.split())
            self.nlp.tagger(text)
        return text

    # Input 1: An original text string parsed by spacy
    # Input 2: A corrected text string parsed by spacy
    # Input 3: A flag for standard Levenshtein alignment
    # Output: An Alignment object
    def align(self, orig, cor, lev=False):
        return Alignment(orig, cor, lev)

    

    # Input: An Edit object
    # Output: The same Edit object with an updated error type
    def classify(self, edit):
        return self.classifier.classify(edit)

    # Input 1: An original text string parsed by spacy
    # Input 2: A corrected text string parsed by spacy
    # Input 3: A flag for standard Levenshtein alignment
    # Input 4: A flag for merging strategy
    # Output: A list of automatically extracted, typed Edit objects
    def annotate(self, orig, cor, lev=False, merging="rules"):
        alignment = self.align(orig, cor, lev)
        edits = self.merge(alignment, merging)
        for edit in edits:
            edit = self.classify(edit)
        return edits
        


    # Input 1: An original text string parsed by spacy
    # Input 2: A corrected text string parsed by spacy
    # Input 3: A token span edit list; [adit type]
    # Output: An Edit object
    def edit_import(self, orig, cor, edit):
    tsv_lines = []
    tsv_lines.append("Phrase originale\tPhrase correcte\Mot erroné\Mot correct\Type d'erreur")
  
    for e in edit:
        error_line = "\t".join([
            orig.text,
            cor.text,
            " ".join([token.text for token in e.o_toks]),
            " ".join([token.text for token in e.c_toks]),
            e.edit_class,
            " ".join(e.type),
            " ".join(e.subtype) if e.subtype is not None and e.subtype != "NA" else ""
        ])
        tsv_lines.append(error_line)
    
    try:
        with open("output.tsv", "w", encoding="utf-8") as file:
            file.write("\n".join(tsv_lines))
        print("TSV file created successfully.")
    except Exception as e:
        print("An error occurred while creating the TSV file:", str(e))
