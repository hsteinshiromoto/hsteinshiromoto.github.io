from __future__ import annotations  # Necessary for self typehint

import re
from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass, field

import nltk
import pandas as pd
from nltk import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer


class Meta(ABC):
    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def make(self):
        pass


class WordList(Meta):
    """_summary_

    Args:
        text (str): Text to get words list from.
        tokenizer (RegexpTokenizer, optional): Word tokenizer. Defaults to RegexpTokenizer(r"\w+").
        stop_words (list[str], optional): List of English stop words. Defaults to stopwords.words("english").

    Example:
        >>> text = "Lorem ipsum dolor sit."
        >>> word_list = WordList(text=text)
        >>> _ = word_list.make()
        >>> word_list.get() == ['Lorem', 'ipsum', 'dolor', 'sit']
        True
    """

    def __init__(
        self,
        text: str,
        tokenizer: RegexpTokenizer = RegexpTokenizer(r"\w+"),
        stop_words: list[str] = stopwords.words("english"),
    ):
        self.text = text
        self.tokenizer = tokenizer
        self.stop_words = stop_words

    def make(self, filter_words: list[str] = []) -> WordList:
        """Makes list of words from text.

        Args:
            filter_words (list[str], optional): Words to be excluded. Defaults to [].

        Returns:
            WordList:
        """
        tokens = self.tokenizer.tokenize(self.text)
        words_list = [w for w in tokens if (w.lower() not in self.stop_words)]

        if filter_words:
            filtered_words = [w for w in words_list if (w.lower() not in filter_words)]
            words_list = filtered_words

        self.words_list = words_list

        return self

    def get(self) -> list[str]:
        """Returns list of words

        Args:
            WordList:

        Returns:
            list[str]: List of words.
        """
        return self.words_list


class NGrams(Meta):
    """Make n-grams, given a words list.

    Args:
        words_list (list[str]): List of words.

    Example:
        >>> text = "Lorem ipsum dolor sit"
        >>> words_list = text.split()
        >>> ngrams = NGrams(words_list)
        >>> _ = ngrams.make(n_grams=2)
        >>> ngrams_obj = ngrams.get()
        >>> [gram for gram in ngrams_obj] == [('Lorem', 'ipsum'), ('ipsum', 'dolor'), ('dolor', 'sit')]
        True
    """

    def __init__(self, words_list: list[str]):
        self.words_list = words_list

    def make(self, n_grams: int = 1) -> NGrams:
        """Make n-grams, given a words list.

        Args:
            n_grams (int, optional): n-grams length. Defaults to 1.

        Returns:
            NGrams:
        """
        self.ngrams = nltk.ngrams(self.words_list, n_grams)

        return self

    def get(self) -> zip:
        """Returns n-grams

        Returns:
            zip: n-grams
        """
        return self.ngrams


@dataclass
class Tags:
    n_grams: zip

    def get_most_frequent_ngram(self, top_frequent: int = 10) -> pd.DataFrame:
        """Get most frequent n-grams

        Args:
            n_grams (zip): N-grams generator.
            top_frequent (int, optional): Select top n_grams. Defaults to 20.

        Returns:
            pd.DataFrame: Top n_grams

        #! TODO: Redo this example
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
        ngrams_freq_dist = nltk.FreqDist(self.n_grams)
        ngrams_count_dict = {"ngrams": [], "count": []}

        for gram, count in ngrams_freq_dist.most_common(top_frequent):
            ngrams_count_dict["ngrams"].append(gram)
            ngrams_count_dict["count"].append(count)

        grams_df = pd.DataFrame.from_dict(ngrams_count_dict)
        grams_df["proportion"] = 100 * grams_df["count"] / grams_df["count"].sum()
        grams_df.sort_values(by="count", inplace=True)

        return grams_df

    def make_tags(self, word_count: Iterable) -> Iterable[str]:
        """_summary_

        Args:
            word_count (Iterable): _description_

        Returns:
            Iterable[str]: _description_

        Example:
            >>> word_count = [("word_1"), ("word_2")]
            >>> make_tags(word_count)
            ['word_1', 'word_2']
            >>> word_count = [("word_1", "word_2"), ("word_3", "word_4")]
            >>> make_tags(word_count)
            ['word_1 word_2', 'word_3 word_4']
        """
        if isinstance(word_count[0], str):
            return word_count

        else:
            return [" ".join(item) for item in word_count]


@dataclass
class CleanContent:
    #! TODO: Continue from here
    content: str
    stop_words: set = field(default_factory=set)
    regex_rules: list = field(default_factory=list[tuple])

    def _make_regex_rules(self):
        default_list = [
            (r"http\S+", "", re.MULTILINE),  # Match website links
            (r"(`{1}(\w+|.+)\b`{1})", "", re.MULTILINE),  # Match inline code blocks
            (r"`{3}\w+((.*|\n|\r)*)(\n|\r)`{3}", "", re.MULTILINE),  # Match code blocks
            (
                r"-\s{1}\[{1}.+\]{1}\({1}.+\){1}",
                "",
                re.MULTILINE,
            ),  # Match table of contents
            (
                r"((\d|\W)+|[^a-zA-Z])",
                " ",
                re.MULTILINE,
            ),  # Match non-word characters and digits
            (r"</?.*?>", " ", re.MULTILINE),  # Match HTML tags
        ]

        if self.regex_rules:
            self.regex_rules = self.regex_rules.extend(default_list)

        else:
            self.regex_rules = default_list

    def get_clear_content(self) -> str:
        text = self.content

        self._make_regex_rules()

        for pattern, substitution, flag in self.regex_rules:
            text = re.sub(pattern, substitution, text, flag)

        return text

    def lemmatize_content(
        self, text: str, lem: WordNetLemmatizer = WordNetLemmatizer()
    ) -> str:
        # 3.5 Convert to list from string
        self.stop_words = self.stop_words or set(stopwords.words("english"))

        text = text.split()

        # 3.7 Lemmatisation
        text = [lem.lemmatize(word) for word in text if not word in self.stop_words]
        return " ".join(text)
