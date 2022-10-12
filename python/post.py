from importlib.resources import contents
from pathlib import Path
from typing import Union

import click
import nltk
import pandas as pd
import yaml

nltk.download("stopwords")
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

nltk.download("wordnet")
import re

from nltk.stem.wordnet import WordNetLemmatizer

nltk.download("genesis")
nltk.download("omw-1.4")

PROJECT_ROOT = Path(__file__).resolve().parents[1]


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

    # 3.1 Remove the non-word alphabets from the sentence
    text = re.sub("[^a-zA-Z]", " ", content)

    # 3.2 Convert to lowercase
    text = text.lower()

    # 3.3 Remove HTML tags
    text = re.sub("</?.*?>", " <> ", text)

    # 3.4 remove non-word characters and digits
    text = re.sub("(\d|\W)+", " ", text)

    # 3.5 Convert to list from string
    text = text.split()

    # 3.7 Lemmatisation
    text = [lem.lemmatize(word) for word in text if not word in stop_words]
    text = " ".join(text)
    word_list.append(text)

    return word_list


def get_content_and_meta(post: str) -> tuple[dict, str]:
    """Gets yaml front page of blog post.

    Args:
        post (str): The blog post containing the yaml front page.

    Returns:
        Union[dict, str]: Yaml Front page and post content

    Example:
        >>> post = "--- title: test --- Test"
        >>> front_page, content = get_content_and_meta(post)
        >>> content == "Test"
        True
        >>> front_page
        {'title': 'test'}
    """
    content = post.split("---")
    metadata = content[1].strip()
    content = content[-1].strip()
    return yaml.safe_load(metadata), content


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

    return freq


@click.command()
@click.option(
    "--filename", "-f", help="Markdown file name to be loaded", type=str, default=None
)
def main(filename: str):
    content = get_post(filename=filename)
    front_page, content = get_content_and_meta(content)
    word_list = process_content(content)
    word_count_df = get_word_counts(word_list)

    print(front_page)
    print(word_count_df)

    return word_count_df, front_page


if __name__ == "__main__":
    main()
