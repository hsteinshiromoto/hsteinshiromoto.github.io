import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.append(str(PROJECT_ROOT))

import src.features.transformers as tf


def main(content: str):

    grams = tf.Grams(content)
    word_list = grams.make_word_list()
    ngrams = grams.make_grams(word_list)
    ngrams_count_df = grams.get_most_frequent_ngram(ngrams)

    pass
