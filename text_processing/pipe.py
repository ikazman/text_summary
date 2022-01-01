import string
import math
from collections import defaultdict
from heapq import nlargest

import pandas as pd
import nltk
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords as nltk_stopwords
from nltk.stem import SnowballStemmer
from pymystem3 import Mystem
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.collocations import QuadgramCollocationFinder
from nltk.metrics.association import QuadgramAssocMeasures

russian_stemmer = SnowballStemmer('russian')

nltk.download('wordnet', quiet=True, raise_on_error=True)
nltk.download('stopwords', quiet=True, raise_on_error=True)
nltk.download('punkt', quiet=True, raise_on_error=True)


class Summary:
    """Класс для процессинга текста и получения результата."""

    def __init__(self, text, file):
        self.mystem = Mystem()
        self.text = text
        self.processed_text = None
        self.summary_length = 1
        self.word_frequency = defaultdict(int)
        self.word_frequency_by_sentence = defaultdict(int)
        self.sentences = 0
        self.sent_scores = {}
        self.summary = None
        self.file_name = file

    def define_summary_length(self):
        """Определяем длину резюме: для текста длинее 20 предложений
        берем десятую часть, иначе - одно предолжение"""
        print(f'\nРезюме для текста {self.file_name}.')
        print('Определяем число предложений для резюме.')
        num_of_sentences = len(sent_tokenize(self.text, language='russian'))
        if num_of_sentences > 20:
            self.summary_length = int(round(num_of_sentences / 10, 0))
        elif num_of_sentences > 9:
            self.summary_length = 3
        else:
            self.summary_length = 1
        print(f'Число предложений в резюме: {self.summary_length}.')

    def clean_text(self):
        """Очищаем текст от знаков препинаний и стоп-слов."""
        print('Очищаем текст от знаков препинаний и стоп-слов.')
        punctuation = string.punctuation + '«»'
        text_without_punct = ''.join(
            [char for char in self.text if char not in punctuation])

        self.processed_text = [word for word in text_without_punct.split()
                               if word.lower()
                               not in nltk_stopwords.words('russian')]

    def lemmatize_and_stem_text(self):
        """Лемматизируем и выделим корень из слов в тексте
        для повышения качества."""
        print('Лемматизируем слова, выделяем корень.')
        temp_text = ' '.join(self.processed_text.copy())
        lemmas = self.mystem.lemmatize(temp_text)
        self.processed_text = [russian_stemmer.stem(lemma) for lemma in lemmas
                               if lemma != ' ']

    def lemmatize_and_stem(self, sentence):
        """Лемматизируем и выделим корень из одного слова."""
        lemma = self.mystem.lemmatize(sentence)
        stemmed_query = [russian_stemmer.stem(word) for word in lemma]
        return ''.join(stemmed_query)

    def count_word_frequency(self):
        """Подсчитываем частоту слов в тексте."""
        print('Подсчитываем частоту слов в тексте.')
        for word in self.processed_text:
            self.word_frequency[word] += 1

    def count_sentences_with_word(self):
        """Подсчитываем важность предложений."""
        print('Подсчитываем обратную частоту.\n')
        sentence_list = sent_tokenize(self.text, language='russian')
        self.sentences = len(sentence_list)
        for sentence in sentence_list:
            sentence_lem = self.lemmatize_and_stem(sentence.lower())
            for word in set(word_tokenize(sentence_lem, language='russian')):
                if word in self.word_frequency.keys():
                    self.word_frequency_by_sentence[word] += 1

    def normilize_word_frequency(self):
        """Нормализуем частоту слов - диапозон от 0 до 1"""
        print('Нормализуем частоту слов - диапозон от 0 до 1.')
        max_freq = max(self.word_frequency.values())
        for word in self.word_frequency.keys():
            self.word_frequency[word] = self.word_frequency[word] / max_freq

    def tf_ifd_score(self):
        for word in self.word_frequency.keys():
            print('WORD - ', word)
            print(self.word_frequency[word])
            print(self.word_frequency_by_sentence[word])
            if self.word_frequency_by_sentence[word] > 0:
                self.word_frequency[word] = abs(math.log((self.word_frequency[word] / len(self.processed_text)) * self.word_frequency_by_sentence[word], 10))
            print(self.word_frequency[word])

    def count_sentenses_score(self):
        """Подсчитываем важность предложений."""
        print('Подсчитываем важность предложений.\n')
        sentence_list = sent_tokenize(self.text, language='russian')
        for sentence in sentence_list:
            sentence_lem = self.lemmatize_and_stem(sentence.lower())
            for word in word_tokenize(sentence_lem, language='russian'):
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
        self.lemmatize_and_stem_text()
        self.count_word_frequency()
        self.count_sentences_with_word()
        self.tf_ifd_score()
        self.normilize_word_frequency()
        self.count_sentenses_score()
        self.summary = ' '.join(nlargest(self.summary_length,
                                         self.sent_scores,
                                         key=self.sent_scores.get))
        print(f'Резюме для {self.file_name} готово.\n' + '-------------------')
