import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer


def create_wordcloud(vocab):

    wordcloud = WordCloud(
        width=800, height=400, background_color="white"
    ).generate_from_frequencies(vocab)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def clean_text(text):
    return " ".join([i for i in text if i.isalpha()])


def create_vocab(topics):
    return TfidfVectorizer().fit_transform(topics)
