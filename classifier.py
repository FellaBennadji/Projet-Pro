import spacy # For linguistic informations
import spacy.symbols as POS # Part Of Speech tags


def classify(edit):
  if edit.o_str != edit.c_str:
    cat = get_two_sided_type(edit.o_tok, edit.c_tok)
    edit.type = cat
  return edit


# First, get edit linguistic informations
# Input: Spacy tokens
# Output: A list of pos tag strings
def get_edit_info(toks):
    pos = []
    for tok in toks:
        p = tok.tag_.split("_")[0]
        pos.append(p)
    return pos


# Output Plur, Sing (number)
def get_number(tag):
    tag = tag.split("__")[-1]
    for t in tag.split("|"):
        attribute, value = t.split("=")
        if attribute == "Number":
            return value
    return ""


# Output Masc, Fem (gender)
def get_gender(tag):
    tag = tag.split("__")[-1]
    for t in tag.split("|"):
        attribute, value = t.split("=")
        if attribute == "Gender":
            return value
    return ""


def get_two_sided_type(o_tok, c_tok):
    # Extract pos tags from the toks as lists
    o_pos = get_edit_info(o_tok)
    c_pos = get_edit_info(c_tok)

    # Same POS on both sides
    if o_pos == c_pos :
      # Adjective agreement
        if c_pos[0] == "ADJ" and o_tok[0].lemma == c_tok[0].lemma :
            
            # Adjective gender agreement
            if get_gender(o_tok[0].tag_) != get_gender(c_tok[0].tag_):
                return 'Accord-Adjectif:Genre'
                
            # Adjective number agreement
            if get_number(o_tok[0].tag_) != get_number(c_tok[0].tag_):
                return 'Accord-Adjectif:Nombre'
