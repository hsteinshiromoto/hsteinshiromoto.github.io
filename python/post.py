import re
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict

import click
import nltk
import pandas as pd
import yaml
from nltk import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

nltk.download("stopwords", "wordnet", "genesis", "omw-1.4")

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class Prepender:
    """Prepend string to file

    Returns:
        None:

    Example:
        >>> with Prepender('test_d.out') as f:
        ...     f.write('string 1\n')
        ...     f.write('string 2\n')
        ...     f.write('string 3\n')

    References:
        [1] https://stackoverflow.com/questions/2677617/write-at-beginning-of-file
    """

    def __init__(self, fname: str, mode="w") -> None:
        """_summary_

        Args:
            fname (str): Filename to be prepended.
            mode (str, optional): Open file mode. Defaults to "w".

        Returns:
            None:
        """
        self.__write_queue = []
        self.__f = open(fname, mode)

    def write(self, s: str) -> None:
        """Write string to file

        Args:
            s (str): String to be written to file

        Returns:
            None:
        """
        self.__write_queue.insert(0, s)

    def close(self):
        self.__exit__(None, None, None)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.__write_queue:
            self.__f.writelines(self.__write_queue)
        self.__f.close()


@dataclass
class Post:
    title: str
    date: datetime
    categories: Iterable[str]
    content: str
    tags: Iterable[str]
    filename: str = ""
    front_page: dict = field(default_factory=lambda: {})


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


def make_filename_from_title(date: datetime, title: str) -> str:
    """Adjust title to filename.

    Args:
        date (datetime):
        title (str):

    Returns:
        str: filename

    Example:
        >>> title = "The Title"
        >>> date = datetime.strptime('2022-10-24', "%Y-%m-%d")
        >>> make_filename_from_title(date, title)
        '2022-10-24-blog-post_the_title'
    """
    return f"{date.strftime('%Y-%m-%d')}-blog-post_{title.lower().replace(' ', '_')}"


def make_front_page(
    date: datetime, title: str, categories: list[str], tags: list[str]
) -> dict:
    """Makes post front page yaml.

    Args:
        date (datetime): Post date.
        title (str): Post title.
        categories (list[str]): Post categories.
        tags (list[str]): Post tags.

    Returns:
        None:

    Example:
        >>> title = "The Title"
        >>> date = datetime.strptime('2022-10-24', "%Y-%m-%d")
        >>> make_front_page(date, title, ['category_1', 'category_2'], ['tag_1', 'tag_2'])
        {'title': 'The Title', 'categories': ['category_1', 'category_2'], 'tags': ['tag_1', 'tag_2'], 'date': '2022-10-24', 'permalink': 'posts/2022/10/24/blog-post_the_title'}
    """

    formatted_title = title.lower().replace(" ", "_")

    permalink = f"posts/{date.strftime('%Y/%m/%d')}/blog-post_{formatted_title}"

    return {
        "title": title,
        "categories": categories,
        "tags": tags,
        "date": date.strftime("%Y-%m-%d"),
        "permalink": permalink,
    }


def get_post(filename: str, path: Path = PROJECT_ROOT / "_posts") -> str:

    with open(str(path / filename)) as file:
        return file.read()


def process_content(
    content: str,
    stop_words: set = set(stopwords.words("english")),
    lem: WordNetLemmatizer = WordNetLemmatizer(),
) -> list:
    """Pre process post content.

    Args:
        content (str): Blog post content.
        stop_words (set, optional): Stop words to be removed. Defaults to set(stopwords.words("english")).
        lem (WordNetLemmatizer, optional): Lemmatizer. Defaults to WordNetLemmatizer().

    Returns:
        list: List of words of post content.
    """

    word_list = []

    regex_apply_dict = {
        r"http\S+": "",  # Remove website links
        r"(`{1}(\w+)`{1})": "",  # Remove inline code
        r"`{3}((.|\n|\r)*)`{3}": "",  # Remove code blocks
        "[^a-zA-Z]": " ",  # Remove the non-word alphabets from the sentence
        "</?.*?>": " <> ",  # Remove HTML tags
        "(\d|\W)+": " ",  # Remove non-word characters and digits
    }

    text = content

    for pattern, substitution in regex_apply_dict.items():
        text = re.sub(pattern, substitution, text)

    # 3.5 Convert to list from string
    text = text.split()

    # 3.7 Lemmatisation
    text = [lem.lemmatize(word) for word in text if not word in stop_words]
    text = " ".join(text)
    word_list.append(text)

    return word_list


def get_content_and_metadata(post: str) -> tuple[dict, str]:
    """Gets yaml front page of blog post.

    Args:
        post (str): The blog post containing the yaml front page.

    Returns:
        Union[dict, str]: Yaml Front page and post content

    Example:
        >>> post = "--- title: test --- Test"
        >>> front_page, content = get_content_and_metadata(post)
        >>> content == "Test"
        True
        >>> front_page
        {'title': 'test'}
        >>> post = "Just a test string"
        >>> front_page, content = get_content_and_metadata(post)
        >>> content == post
        True
        >>> front_page
        {}
    """
    regex = r"-{3}\n{1}((.|\n)*)-{3}\n{1}"
    result = re.search(regex, post, re.MULTILINE)

    if result:
        content = re.sub(regex, "", post)
        metadata = result.group()
        metadata = yaml.safe_load(metadata)

    else:
        content = post
        metadata = {}

    return metadata, content


def get_word_counts(word_list: list) -> pd.DataFrame:
    """_summary_

    Args:
        word_list (list): List of words.

    References:
        [1] https://medium.com/a-layman/pre-process-data-with-nltk-and-create-a-tag-cloud-for-blog-posts-in-react-a69025f4507c

    Returns:
        pd.DataFrame: Frequency of each word.

    Example:
        >>> word_list = ['A', 'B', 'C', 'D']
        >>> freq = get_word_counts(word_list)
        >>> freq["Count"].values.tolist()
        [1, 1, 1, 1]
        >>> freq["Proportion"].values.tolist()
        [25.0, 25.0, 25.0, 25.0]
    """

    # 4. Caculate the number of occurrences
    freq = pd.Series(" ".join(word_list).split()).value_counts()
    freq.index.name = "Word"
    freq = freq.to_frame(name="Count").reset_index()
    freq["Proportion"] = 100 * freq["Count"] / freq["Count"].sum()
    freq.sort_values(by="Count", inplace=True)

    return freq


def make_tags(word_count: Iterable) -> Iterable[str]:
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


def get_title(post: str) -> str:
    """Get title of post. Where it is assumed to be the first line.

    Args:
        post (str): Blog post content.

    Returns:
        str: Post title.
    """
    raw_title = post.partition("\n")[0]
    return raw_title.replace("#", "").strip()



    with open(str(path / filename), "r+") as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip("\r\n") + "\n" + content)


@click.command()
@click.option(
    "--filename", "-f", help="Markdown file name to be loaded", type=str, required=True
)
@click.option("--date", "-d", help="Blog post date", type=datetime, required=False)
@click.option(
    "--categories", "-c", help="Post categories", type=Iterable[str], required=False
)
@click.option("--n_tags", "-n", help="Number of tags", type=int, required=False)
def main(
    filename: str,
    date: datetime = None,  # type: ignore
    categories: Iterable[str] = [],
    n_tags: int = 5,
):
    date = date or datetime.now().date()

    post = get_post(filename=filename)
    title = get_title(post)
    front_page, content = get_content_and_metadata(post)

    word_list = process_content(content)
    word_count_df = get_word_counts(word_list)
    tags = make_tags(word_count_df["Word"].tolist(), n_tags)

    front_page = front_page or make_front_page(date, title, categories, tags)

    post = Post(
        title=title,
        date=date,
        categories=categories,
        content=content,
        tags=tags,
    )

    print(front_page)
    print(word_count_df)

    return word_count_df, front_page


if __name__ == "__main__":
    main()
