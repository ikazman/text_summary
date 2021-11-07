import string
from heapq import nlargest

import nltk
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords as nltk_stopwords

nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')


class Summary:
    """Класс для процессинга текста и получения результата."""

    def __init__(self, text):
        self.text = text
        self.processed_text = None
        self.summary_length = 1
        self.word_frequency = {}
        self.sent_scores = {}
        self.summary = None

    def define_summary_length(self):
        """Определяем длину резюме: для текста длинее 20 предложений
        берем десятую часть, иначе - одно предолжение"""
        num_of_sentences = self.text.count('. ')
        if num_of_sentences > 20:
            self.summary_length = int(round(num_of_sentences / 10, 0))
        else:
            self.summary_length = 1

    def clean_text(self):
        """Очищаем текст от знаков препинаний и стоп-слов."""
        text_without_punct = ''.join(
            [char for char in self.text if char not in string.punctuation])

        self.processed_text = [word for word in text_without_punct.split()
                               if word.lower()
                               not in nltk_stopwords.words('russian')]

    def count_word_frequency(self):
        """Подсчитываем частоту слов в тексте."""
        for word in self.processed_text:
            if word not in self.word_frequency:
                self.word_frequency[word] = 1
            else:
                self.word_frequency[word] += 1

    def normilize_word_frequency(self):
        """Нормализуем частоту слов - диапозон от 0 до 1"""
        max_freq = max(self.word_frequency.values())
        for word in self.word_frequency.keys():
            self.word_frequency[word] = self.word_frequency[word] / max_freq

    def count_sentenses_score(self):
        """Подсчитываем важность предложений."""
        sentence_list = sent_tokenize(self.text)
        for sentence in sentence_list:
            for word in word_tokenize(sentence.lower()):
                if word in self.word_frequency.keys():
                    if sentence not in self.sent_scores.keys():
                        self.sent_scores[sentence] = self.word_frequency[word]
                    else:
                        self.sent_scores[sentence] += self.word_frequency[word]

    def get_summary(self):
        """Получаем резюме из текста: самые важные предложения исходя из
        частоты слов."""
        self.define_summary_length()
        self.clean_text()
        self.count_word_frequency()
        self.normilize_word_frequency()
        self.count_sentenses_score()
        self.summary = ' '.join(nlargest(self.summary_length,
                                         self.sent_scores,
                                         key=self.sent_scores.get))
