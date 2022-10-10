from importlib.resources import contents
from pathlib import Path
import pandas as pd

import nltk

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


def get_word_counts(content: str) -> pd.DataFrame:
    """_summary_

    Args:
        content (str): _description_

    References:
        [1] https://medium.com/a-layman/pre-process-data-with-nltk-and-create-a-tag-cloud-for-blog-posts-in-react-a69025f4507c

    Returns:
        pd.DataFrame: _description_
    """

    stop_words = set(stopwords.words("english"))
    res = []

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

    # 3.6 Stemming
    ps = PorterStemmer()

    # 3.7 Lemmatisation
    lem = WordNetLemmatizer()
    text = [lem.lemmatize(word) for word in text if not word in stop_words]
    text = " ".join(text)
    res.append(text)

    # 4. Caculate the number of occurrences
    freq = pd.Series(" ".join(res).split()).value_counts()
    freq.index.name = "Word"
    freq = freq.to_frame(name="Count").reset_index()
    freq["Proportion"] = 100 * freq["Count"] / freq["Count"].sum()

    return freq


def main(blog_post: str):
    content = get_post(filename=blog_post)
    word_count_df = get_word_counts(content)

    return word_count_df


if __name__ == "__main__":
    word_count_df = main(
        "22022-10-31-blog-post_are_model_performance_metrics_enough.md"
    )

    print(word_count_df)
