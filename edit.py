class Edit:

    # Input 1: An original text string parsed by spacy
    # Input 2: A corrected text string parsed by spacy
    # Input 4: An error type string, if known
    def __init__(self, orig, cor, edit, type="NA"):
        # Orig offsets, spacy tokens and string
        self.o_tok = edit[0]
        self.o_str = self.o_tok.text if self.o_tok else ""
        # Cor offsets, spacy tokens and string
        self.c_tok = edit[1]
        self.c_str = self.c_tok.text if self.c_tok else ""
        # Error type
        self.type = type



    # Edit object string representation
    def __str__(self):
        orig = "Orig: "+str([self.o_str])
        cor = "Cor: "+str([self.c_str])
        type = "Type: "+repr(self.type)
        attributes = [orig, cor, type]
        return ", ".join(attributes)
