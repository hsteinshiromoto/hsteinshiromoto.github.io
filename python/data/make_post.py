import sys
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Union

import click
import frontmatter
import nltk
import yaml
from transformers import pipeline

nltk.download("stopwords", "wordnet", "genesis", "omw-1.4")

PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.append(str(PROJECT_ROOT))

import python.features.build_features as bf


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


def get_post(filename: str, path: Path = PROJECT_ROOT / "_posts") -> tuple[str, dict]:

    with open(str(path / filename)) as file:
        post = frontmatter.load(file)

    return post.content, post.metadata


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

    content, front_page = get_post(filename=filename)
    title = get_title(content)

    if not front_page:
        front_page = bf.main(content, date, title, categories)

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
