from dataclasses import dataclass, field

import nltk
import pandas as pd
from nltk import RegexpTokenizer
from nltk.corpus import stopwords


@dataclass
class Grams:
    """_summary_

    Returns:
        _type_: _description_
    """

    text: str
    tokenizer: RegexpTokenizer = RegexpTokenizer(r"\w+")
    stpwords: list = field(default_factory=list)

    def make_word_list(self, filter_words: list = []) -> list:
        """Make list of words from text

        Args:
            n_gram (int): n gram size.
            filter_words (list, optional): Words to be excluded. Defaults to [].

        Returns:
            list: Words list.

        Example:
            >>> text = "Lorem ipsum dolor sit."
            >>> gram = Grams(text=text)
            >>> gram.make_word_list(1)
            ['Lorem', 'ipsum', 'dolor', 'sit']
        """
        tokens = self.tokenizer.tokenize(self.text)

        self.stpwords = self.stpwords or stopwords.words("english")
        words_list = [w for w in tokens if (w.lower() not in self.stpwords)]

        if filter_words:
            filtered_words = [w for w in words_list if (w.lower() not in filter_words)]
            words_list = filtered_words

        return words_list

    def make_grams(self, words_list: list, n_grams: int = 1) -> zip:
        """Make n-grams, given a words list.

        Args:
            words_list (list): List of words
            n_grams (int, optional): n-grams length. Defaults to 1.

        Returns:
            zip: N-grams generator.

        Example:
            >>> text = "Lorem ipsum dolor sit."
            >>> gram = Grams(text=text)
            >>> words_list = gram.make_word_list()
            >>> ngrams = gram.make_grams(words_list, n_grams=2)
            >>> [gram for gram in ngrams]
            [('Lorem', 'ipsum'), ('ipsum', 'dolor'), ('dolor', 'sit')]
        """
        return nltk.ngrams(words_list, n_grams)

    def get_most_frequent_ngram(
        self, n_grams: zip, top_frequent: int = 20
    ) -> pd.DataFrame:
        """Get most frequent n-grams

        Args:
            n_grams (zip): N-grams generator.
            top_frequent (int, optional): Select top n_grams. Defaults to 20.

        Returns:
            pd.DataFrame: Top n_grams

        Example:
            >>> text = "Lorem ipsum dolor sit. Lorem ipsum, dolor sit."
            >>> gram = Grams(text=text)
            >>> words_list = gram.make_word_list()
            >>> ngrams = gram.make_grams(words_list, n_grams=2)
            >>> ngrams_df = gram.get_most_frequent_ngram(ngrams, 2)
            >>> output = pd.DataFrame.from_dict({'ngrams': [('Lorem', 'ipsum'), ('ipsum', 'dolor')], 'count': [2]*2, 'proportion': [50.0]*2})
            >>> ngrams_df.equals(output)
            True
        """
        ngrams_freq_dist = nltk.FreqDist(n_grams)
        ngrams_count_dict = {"ngrams": [], "count": []}

        for gram, count in ngrams_freq_dist.most_common(top_frequent):
            ngrams_count_dict["ngrams"].append(gram)
            ngrams_count_dict["count"].append(count)

        grams_df = pd.DataFrame.from_dict(ngrams_count_dict)
        grams_df["proportion"] = 100 * grams_df["count"] / grams_df["count"].sum()
        grams_df.sort_values(by="count", inplace=True)

        return grams_df
