from crawler.algos import filter_urls, most_used_phrase


def test_most_used_phrase():
    text = "Machine learning is a black boxes with unicorns." \
        "Humans are the real black boxes, at least as far as machine learning is concerned."

    assert most_used_phrase(text) == "machine learning"


def test_filter_urls():
    text = "sample http://domain/test text"
    assert filter_urls(text) == "sample  text"
