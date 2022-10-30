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


class Meta(abc):
    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def make(self):
        pass


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
