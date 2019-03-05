import re
from collections import Counter

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer


def most_used_phrase(text):
    tokenizer = RegexpTokenizer(r"\w+")
    words = tokenizer.tokenize(text.lower())
    tokens = []
    for word in words:
        if word not in set(stopwords.words('english')):
            tokens.append(word)
    bigrams = nltk.bigrams(tokens)
    common = most_common(list(bigrams))[0]
    return " ".join(common)


def filter_urls(text):
    url_regex = r"https?:\/\/(.*)\/(\w+)?"
    return re.sub(url_regex, "", text)


def most_common(items, count=1):
    results = Counter(items).most_common(count)
    return [item for item, count in results]
