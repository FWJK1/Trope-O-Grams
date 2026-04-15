import regex as re
import pandas as pd
import numpy as np


def import_hedonometer_as_dict():
    labmt_df = pd.read_csv("Data/Hedonometer.csv")
    labmt_dict = dict(zip(labmt_df["Word"], labmt_df["Happiness Score"]))
    return labmt_dict


def parse_text(text):
    if type(text) is not str:
        return None
    ## remove underscores used for emphasis
    text = re.sub(r"\[.*?\]", "", text)  # remove square brackets.
    text = re.sub(r"_", "", text)

    ## replace curse words
    text = re.sub(r"(?i)D--N", "Damn", text, flags=re.IGNORECASE)

    ## separate out basic punctuation
    pattern = r"[!?.,:;]"  # Match any of the punctuation marks
    text = re.sub(pattern, r" \g<0> ", text)

    ## isolate paranthesis
    pattern = r"[\(\)]"
    text = re.sub(pattern, r" \g<0> ", text)

    ## standardize dashes
    pattern = r"(----|--|;-|[—])"
    text = re.sub(pattern, r" --- ", text)

    ## fix specific salutations we broke by separating out punctuation
    text = re.sub(r"Mr .", r"Mr.", text)
    text = re.sub(r"Mrs .", r"Mrs.", text)
    text = re.sub(r"Dr .", r"Dr.", text)

    ## clean up white space duplication
    text = re.sub(r"\s+", r" ", text)

    # Add a space before opening quotes, except for em dashes (handling edge case)
    text = re.sub(
        r'(?<!—)\s"', ' " ', text
    )  # Add space before regular opening quotes (")
    text = re.sub(
        r"(?<!—)\s“", " “ ", text
    )  # Add space before opening curly quotes (left)
    text = re.sub(
        r"(?<!—)\s”", " ” ", text
    )  # Add space before opening curly quotes (right)

    # add a space before closing quotes as well
    text = re.sub(r'"', ' " ', text)  # Closing quotes (regular)
    text = re.sub(r"“", " “ ", text)  # Closing curly quotes (left)
    text = re.sub(r"”", " ” ", text)  # Closing curly quotes (right)

    ## clean up white space duplication
    text = re.sub(r"\s+", r" ", text)

    ## screwing around with single quotes
    text = re.sub(r"‘", " ' ", text)
    text = re.sub(r"’", " ' ", text)
    text = re.sub(r"(\s)'(\p{L})", r"\1' \2", text)
    text = re.sub(r"(\p{L})'(\s)", r"\1 ' \2", text)

    ## remove any illustration descriptions within square brackets
    # text = re.sub(r'\[.*?illustration.*?\]', '', text, flags=re.IGNORECASE)

    ## handle possession indicator
    text = re.sub(r"'s", " 's ", text)

    ## turn the text into a list
    text = text.split()
    return text
