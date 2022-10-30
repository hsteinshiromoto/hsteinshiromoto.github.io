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
        >>> word_list = WordList()
        >>> _ = word_list.make(text=text)
        >>> word_list.get() == ['Lorem', 'ipsum', 'dolor', 'sit']
        True
    """

    def __init__(
        self,
        tokenizer: RegexpTokenizer = RegexpTokenizer(r"\w+"),
        stop_words: list[str] = stopwords.words("english"),
    ):
        self.tokenizer = tokenizer
        self.stop_words = stop_words

    def make(self, text: str, filter_words: list[str] = []) -> WordList:
        """Makes list of words from text.

        Args:
            filter_words (list[str], optional): Words to be excluded. Defaults to [].

        Returns:
            WordList:
        """
        tokens = self.tokenizer.tokenize(text)
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

    Example:
        >>> text = "Lorem ipsum dolor sit"
        >>> words_list = text.split()
        >>> ngrams = NGrams()
        >>> _ = ngrams.make(words_list=words_list, n_grams=2)
        >>> ngrams_obj = ngrams.get()
        >>> [gram for gram in ngrams_obj] == [('Lorem', 'ipsum'), ('ipsum', 'dolor'), ('dolor', 'sit')]
        True
    """

    def make(self, words_list: list[str], n_grams: int = 1) -> NGrams:
        """Make n-grams, given a words list.

        Args:
            words_list (list[str]): List of words.
            n_grams (int, optional): n-grams length. Defaults to 1.

        Returns:
            NGrams:
        """
        self.ngrams = nltk.ngrams(words_list, n_grams)

        return self

    def get(self) -> zip:
        """Returns n-grams

        Returns:
            zip: n-grams
        """
        return self.ngrams


class Tags(Meta):
    """Create post tags.

    Example:
        >>> text = "Lorem ipsum dolor sit. Lorem ipsum, dolor sit."
        >>> grams = [('Lorem', 'ipsum'), ('ipsum', 'dolor'), ('dolor', 'sit')]
        >>> tags = Tags()
        >>> _ = tags.make(grams, 2)
        >>> tags.get()
        ['Lorem ipsum', 'ipsum dolor']
        >>> grams = [("word_1"), ("word_2")]
        >>> tags = Tags()
        >>> _ = tags.make(grams, 2)
        >>> tags.get()
        ['word_1', 'word_2']
    """

    def make(self, n_grams: zip, top_frequent: int = 5) -> Tags:
        """Get most frequent n-grams

        Args:
            n_grams (zip): N-grams generator.
            top_frequent (int, optional): Select top n_grams. Defaults to 5.

        Returns:
            Tags:
        """
        ngrams_freq_dist = nltk.FreqDist(n_grams)
        ngrams_count_dict = {"ngrams": [], "count": []}

        for gram, count in ngrams_freq_dist.most_common(top_frequent):
            ngrams_count_dict["ngrams"].append(gram)
            ngrams_count_dict["count"].append(count)

        grams_df = pd.DataFrame.from_dict(ngrams_count_dict)
        grams_df["proportion"] = 100 * grams_df["count"] / grams_df["count"].sum()
        grams_df.sort_values(by="count", inplace=True)

        self.grams_df = grams_df

        return self

    def get(self) -> Iterable[str]:
        """Returns n tags according to frequency.

        Returns:
            Iterable[str]: n tags.
        """
        if isinstance(self.grams_df.loc[0, "ngrams"], str):
            return self.grams_df["ngrams"].tolist()

        else:
            return [" ".join(item) for item in self.grams_df["ngrams"].tolist()]


class RegexContentFilter(Meta):
    def make(self, regex_rules: list[tuple] = []):
        """_summary_

        Args:
            regex_rules (list[tuple], optional): _description_. Defaults to [].

        Returns:
            RegexContentFilter:
        """
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

        if regex_rules:
            self.regex_rules = regex_rules.extend(default_list)

        else:
            self.regex_rules = default_list

        return self

    def get(self, content: str) -> str:
        filtered_text = content
        for pattern, substitution, flag in self.regex_rules:
            filtered_text = re.sub(pattern, substitution, filtered_text, flag)

        return filtered_text


    def lemmatize_content(
        self, text: str, lem: WordNetLemmatizer = WordNetLemmatizer()
    ) -> str:
        # 3.5 Convert to list from string
        self.stop_words = self.stop_words or set(stopwords.words("english"))

        text = text.split()

        # 3.7 Lemmatisation
        text = [lem.lemmatize(word) for word in text if not word in self.stop_words]
        return " ".join(text)
