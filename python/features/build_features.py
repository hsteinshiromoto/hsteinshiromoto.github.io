import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.append(str(PROJECT_ROOT))

import python.features.transformers as tf


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


def main(post: str, date: datetime, title: str, categories: list[str]):

    n_grams_steps = [
        ("filter_content", tf.RegexContentFilter()),
        ("lemmatize_content", tf.LemmatizeContent()),
        ("get_word_list", tf.WordList()),
        ("get_ngrams", tf.NGrams()),
    ]

    n_grams_pipeline = tf.Pipeline(n_grams_steps)

    _ = n_grams_pipeline.make(post)
    ngrams = n_grams_pipeline.get(post)

    tags = tf.Tags(5)
    _ = tags.make(ngrams)
    post_tags = tags.get(ngrams)

    front_page = make_front_page(date, title, categories, post_tags)

    return front_page


if __name__ == "__main__":
    main()
