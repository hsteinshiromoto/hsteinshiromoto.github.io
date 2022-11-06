from __future__ import annotations  # Necessary for self typehint

import re
from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Callable, Generator

import nltk
import numpy as np
import pandas as pd
from nltk import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer as SKLCountVectorizer


class Meta(ABC):
    @abstractmethod
    def make(self):
        pass

    @abstractmethod
    def get(self):
        pass


class CountVectorizer(Meta, SKLCountVectorizer):
    """Get count vector of ngrams in text.

    Example:
        >>> text = ("Lorem ipsum dolor sit amet.",
        ... "Lorem dolor Tincidunt praesent semper")
        >>> cv = CountVectorizer()
        >>> _ = cv.make(text)
        >>> list(cv.get(text))
        [(1, 'amet'), (2, 'dolor'), (1, 'ipsum'), (2, 'lorem'), (1, 'praesent'), (1, 'semper'), (1, 'sit'), (1, 'tincidunt')]
    """

    def __init__(self) -> None:
        """
        Args:
            See [1]

        References:
            [1] https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
        """
        super().__init__()

    def make(self, text: str) -> CountVectorizer:
        self.fit(text)

    def get(self, text: str) -> zip:
        count_array = self.transform(text).sum(axis=0)
        count_array = np.asarray(count_array).reshape(-1)
        return zip(count_array, self.get_feature_names_out())


class Pipeline:
    """Text processing pipeline

    Example:
        >>> class test_1:
        ...     def make(self, a):
        ...         return self
        ...     def get(self, a):
        ...         return 2*a
        >>> class test_2:
        ...     def make(self, a):
        ...         return self
        ...     def get(self, a):
        ...         return 3*a
        >>> input = 1
        >>> pipe = Pipeline([("test_1", test_1()), ("test_2", test_2())])
        >>> pipe.make(input)
        >>> pipe.get(input) == 6
        True
    """

    def __init__(self, steps: list[tuple[str, Callable]]) -> None:
        self.steps = steps

    def make(self, text: str = ""):
        for index, (step, func) in enumerate(self.steps):
            self.steps[index] = (step, func.make(text))

    def get(self, text: str = ""):
        for _, func in self.steps:
            try:
                output = func.get(output)

            except (NameError, UnboundLocalError):
                output = func.get(text)

        return output


class WordList(Meta):
    """Makes list of words from text using regex tokenizer.

    Args:
        tokenizer (RegexpTokenizer, optional): Word tokenizer. Defaults to RegexpTokenizer(r"\w+").
        stop_words (list[str], optional): List of English stop words. Defaults to stopwords.words("english").
        filter_words (list[str], optional): Words to be excluded. Defaults to [].

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
        filter_words: list[str] = [],
    ):
        self.tokenizer = tokenizer
        self.stop_words = stop_words
        self.filter_words = filter_words

    def make(self, text: str) -> WordList:
        """Makes list of words from text.

        Args:
            text (str): Text to get words list from.

        Returns:
            WordList:
        """
        tokens = self.tokenizer.tokenize(text)
        words_list = [
            w for w in tokens if (w.lower() not in self.stop_words) & (len(w) > 1)
        ]

        if self.filter_words:
            filtered_words = [
                w for w in words_list if (w.lower() not in self.filter_words)
            ]
            words_list = filtered_words

        self.words_list = words_list

        return self

    def get(self, text="") -> list[str]:
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
        >>> ngrams = NGrams(n_grams=2)
        >>> _ = ngrams.make()
        >>> ngrams_obj = ngrams.get(words_list)
        >>> [gram for gram in ngrams_obj] == [('Lorem', 'ipsum'), ('ipsum', 'dolor'), ('dolor', 'sit')]
        True
    """

    def __init__(self, n_grams: int = 1):
        """Make n-grams, given a words list.

        Args:
            n_grams (int, optional): n-grams length. Defaults to 1.
        """
        self.n_grams = n_grams

    def make(self, text: str = "") -> NGrams:
        """Make n-grams, given a words list.

        Returns:
            NGrams:
        """
        return self

    def get(self, words_list: list[str]) -> Generator:
        """Returns n-grams

        Args:
            words_list (list[str]): List of words.

        Returns:
            Generator: n-grams
        """
        return nltk.ngrams(words_list, self.n_grams)


class Tags(Meta):
    """Create post tags.

    Example:
        >>> text = "Lorem ipsum dolor sit. Lorem ipsum, dolor sit."
        >>> grams = [('Lorem', 'ipsum'), ('ipsum', 'dolor'), ('dolor', 'sit')]
        >>> tags = Tags(2)
        >>> _ = tags.make(grams)
        >>> tags.get()
        ['Lorem ipsum', 'ipsum dolor']
        >>> grams = [("word_1"), ("word_2")]
        >>> tags = Tags(2)
        >>> _ = tags.make(grams)
        >>> tags.get()
        ['word_1', 'word_2']
    """

    def __init__(self, top_frequent: int = 5) -> None:
        """_summary_

        Args:
            top_frequent (int, optional): Select top n_grams. Defaults to 5.
        """
        self.top_frequent = top_frequent

    def make(
        self,
        n_grams: zip,
    ) -> Tags:
        """Get most frequent n-grams

        Args:
            n_grams (zip): N-grams generator.

        Returns:
            Tags:
        """
        ngrams_freq_dist = nltk.FreqDist(n_grams)
        ngrams_count_dict = {"ngrams": [], "count": []}

        for gram, count in ngrams_freq_dist.most_common(self.top_frequent):
            ngrams_count_dict["ngrams"].append(gram)
            ngrams_count_dict["count"].append(count)

        grams_df = pd.DataFrame.from_dict(ngrams_count_dict)
        grams_df["proportion"] = 100 * grams_df["count"] / grams_df["count"].sum()
        grams_df.sort_values(by="count", inplace=True)

        self.grams_df = grams_df

        return self

    def get(self, text="") -> Iterable[str]:
        """Returns n tags according to frequency.

        Returns:
            Iterable[str]: n tags.
        """
        if isinstance(self.grams_df.loc[0, "ngrams"], str):
            return self.grams_df["ngrams"].tolist()

        else:
            return [" ".join(item) for item in self.grams_df["ngrams"].tolist()]


class RegexContentFilter(Meta):
    """Removes regular expressions from text.

    Example:
        >>> text = "http://www.google.com/index.html the `code here` bla bla </tag>"
        >>> content_filter = RegexContentFilter()
        >>> _ = content_filter.make()
        >>> content_filter.get(text)
        'the bla bla tag'
    """

    def __init__(self, regex_rules: list[tuple] = []):
        """Removes regular expressions from text.

        Args:
            regex_rules (list[tuple], optional): List of regexes to be removed (pattern, substitution, regex flags). Defaults to [].
        """
        self.regex_rules = regex_rules

    def make(self, text: str = "") -> RegexContentFilter:
        """Define list of regular expressions based on a default list.

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
            (r"\d*", " ", re.MULTILINE),  # Remove digits
        ]

        if self.regex_rules:
            self.regex_rules = self.regex_rules.extend(default_list)

        else:
            self.regex_rules = default_list

        return self

    def get(self, text: str) -> str:
        """Remove regular expressions from text.

        Args:
            text (str): Text to be filtered.

        Returns:
            str: Filtered text.
        """
        filtered_text = text
        for pattern, substitution, flag in self.regex_rules:
            filtered_text = re.sub(pattern, substitution, filtered_text, flag)

        return filtered_text.strip()


class LemmatizeContent(Meta):
    """Lemmatize post content

    Example:
        >>> text = "Connecting the things"
        >>> lemmatizer = LemmatizeContent()
        >>> _ = lemmatizer.make(text)
        >>> lemmatizer.get()
        'Connecting thing'
    """

    def __init__(
        self,
        stop_words: list[str] = stopwords.words("english"),
        lem: WordNetLemmatizer = WordNetLemmatizer(),
    ):
        """Lemmatizes post content

        Args:
            stop_words (list[str], optional): List of English stop words. Defaults to stopwords.words("english").
            lem (WordNetLemmatizer, optional): Word lemmatizer. Defaults to WordNetLemmatizer().
        """
        self.stop_words = set(stop_words)
        self.lem = lem

    def make(
        self,
        text: str,
    ) -> LemmatizeContent:
        """Lemmatizes words in post content.

        Args:
            content (str): Post content.
        """
        content = text.split()

        # 3.7 Lemmatisation
        self.text = [
            self.lem.lemmatize(word) for word in content if not word in self.stop_words
        ]

        return self

    def get(self, text="") -> str:
        """Get post text with lemmatized words

        Returns:
            str: Post text with lemmatized words
        """
        return " ".join(self.text)
