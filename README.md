# NLP Text Alignment and Error Classification
This is the repository of my graduation project. This Python script is designed for Natural Language Processing (NLP) tasks related to text alignment and error classification. It utilizes the spaCy library for linguistic analysis and the Errant library for aligning and classifying edits in text data. The script is particularly useful for tasks like grammatical error detection and correction in parallel texts.

## Features

- Aligns and classifies edits in parallel text data.
- Detects and categorizes adjective agreement errors (gender and number).
- Outputs aligned sentences for further analysis.

## Requirements

- Python 3.x
- spaCy V.2 library (French language model)
- Errant library (for text alignment and error classification)
- pandas library (for data handling)

## Usage

1. Ensure you have the required libraries installed (spaCy V.2, Errant, pandas).
2. Run the script with your input data in TSV (Tab-Separated Values) format.
3. The script will align and classify edits in your data, providing information on adjective agreement errors and producing aligned sentence pairs.
4. The results are saved to a TSV file named `aligned_sentences.tsv`.

## Example

You can run the script by executing the `main()` function in the provided Python file. You'll be prompted to enter the name of the input TSV file containing your data.

```bash
python nlp_alignment.py

# Contact 
For more information about the research methodology and for questions regarding collaboration, please contact: bennadjifella@yahoo.fr

