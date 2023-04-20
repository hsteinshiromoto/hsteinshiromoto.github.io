import sys
from datetime import datetime
from pathlib import Path

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from transformers import pipeline

PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.append(str(PROJECT_ROOT))

import python.features.transformers as tf

DEFAULT_SETTINGS = {
    "CountVectorizer": {
        "strip_accents": "ascii",
        "stop_words": stopwords.words("english"),
        "ngram_range": (1, 3),
    }
}


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
        ("RegexContentFilter", tf.RegexContentFilter()),
        ("LemmatizeContent", tf.LemmatizeContent()),
        ("Tokenizer", tf.Tokenizer(sent_tokenize)),
        (
            "CountVectorizer",
            tf.CountVectorizer(**DEFAULT_SETTINGS["CountVectorizer"]),  # type: ignore
        ),
    ]

    n_grams_pipeline = tf.Pipeline(n_grams_steps)

    _ = n_grams_pipeline.make(post)
    ngrams = n_grams_pipeline.get(post)

    tags = tf.Tags(5)
    _ = tags.make(ngrams)
    post_tags = tags.get(ngrams)

    summarize_text_steps = [
        ("RegexContentFilter", tf.RegexContentFilter()),
        ("GenText", tf.GenText(pipeline("text-generation", model="gpt2"))),
    ]

    summarize_text_pipeline = tf.Pipeline(summarize_text_steps)
    _ = summarize_text_pipeline.make(post)
    summary = summarize_text_pipeline.get(post)

    front_page = make_front_page(date, title, categories, post_tags)

    return front_page


if __name__ == "__main__":
    main()
