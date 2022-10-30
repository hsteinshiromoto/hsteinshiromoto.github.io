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

from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

nltk.download("stopwords", "wordnet", "genesis", "omw-1.4")

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class Prepender:
    """Prepend string to file

    Returns:
        None:

    # Example:
    #     >>> with Prepender('test_d.out') as f:
    #     ...     f.write('string 1\n')
    #     ...     f.write('string 2\n')
    #     ...     f.write('string 3\n')

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


@dataclass
class CleanContent:
    #! TODO: Continue from here
    content: str
    stop_words: set = field(default_factory=set)
    regex_rules: list = field(default_factory=list)

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

        self.regex_rules = (
            self.regex_rules.extend(default_list) if self.regex_rules else default_list
        )

    def get_clear_content(self) -> str:
        text = self.content

        self._make_regex_rules()

        for pattern, substitution, flag in self.regex_rules:
            text = re.sub(pattern, substitution, text, flag)

        return text

    def preprocess_content(
        self, text: str, lem: WordNetLemmatizer = WordNetLemmatizer()
    ) -> str:
        # 3.5 Convert to list from string
        self.stop_words = self.stop_words or set(stopwords.words("english"))

        text = text.split()

        # 3.7 Lemmatisation
        text = [lem.lemmatize(word) for word in text if not word in self.stop_words]
        return " ".join(text)


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


def make_post(frontpage: dict):

    filename = f"{str(date)}_blog_post_{filename_title}.md"

    with Prepender(str(path / filename)) as f:
        f.write("---")
        f.write(yaml.dump(front_page))
        f.write("---")


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

    grams = Grams(content)
    word_list = grams.make_word_list()
    ngrams = grams.make_grams(word_list)
    ngrams_count_df = grams.get_most_frequent_ngram(ngrams)

    tags = make_tags(ngrams_count_df["ngrams"].tolist())

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
