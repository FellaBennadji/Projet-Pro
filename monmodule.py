import errant
import spacy
import pandas as pd

def classify(edit):
   # Nothing to nothing is a detected but not corrected edit
    if edit.o_str != edit.c_str:
      cat = get_two_sided_type(edit.o_toks, edit.c_toks)
      edit.type = cat
      if cat is not None:  # Check if cat is not None (adjective-related error)
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


def main():
    nlp = spacy.load("fr_core_news_lg", disable=["ner"])
    annotator = errant.load('en', nlp)

    nom_fichier = input("Veuillez entrer le nom du fichier TSV : ")

    df = pd.read_csv(nom_fichier, sep='\t', header=None, encoding='windows-1252', dtype=str, na_values=['nan', 'NaN'])
    df.fillna('', inplace=True)  # Remplacer les valeurs NaN par des chaînes vides

    # Créer une colonne avec les phrases correctes suivies des phrases originales, séparées par un saut de ligne
    aligned_sentences = []

    for col_index, col_name in enumerate(df.columns[2:], start=2):
        cor_text = df.iloc[0, col_index]  # Phrase corrigée dans la première ligne de la colonne

        for orig_text in df.iloc[1:, col_index]:  # Phrases originales dans le reste des lignes de la colonne
            # Vérifier si orig_text ou cor_text est vide et ignorer le traitement ultérieur si l'un d'eux est vide
            if not orig_text:
                continue
            orig = annotator.parse(orig_text)
            cor = annotator.parse(cor_text)
            alignment = annotator.align(orig, cor, lev=False)
            edits = annotator.merge(alignment, merging='rules')
            for e in edits:
                e = classify(e)
                if e.type is not None:
                    print(e)


            # Extraire les phrases alignées après la fusion
            orig_aligned = ' | '.join([word.text for word in orig])
            cor_aligned = ' | '.join([word.text for word in cor])

            # Concaténer les phrases correctes suivies des phrases originales avec un saut de ligne entre elles
            aligned_pair = f'Phrase correcte  : {cor_aligned}\n Phrase originale : {orig_aligned}'

            # Ajouter cette paire de phrases à la liste aligned_sentences
            aligned_sentences.append(aligned_pair)

    # Créer un DataFrame avec une seule colonne contenant toutes les phrases alignées
    df_result = pd.DataFrame(aligned_sentences, columns=['aligned_sentences'])

    # Enregistrez le DataFrame dans un fichier TSV
    df_result.to_csv('aligned_sentences.tsv', sep='\t', header=False, index=False, encoding='utf-8')

if __name__ == "__main__":
    main()
