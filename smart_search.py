import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import numpy as np
class SmartSearch:
    def __init__(self, df, vectorizer=None):
        drop_words = ['Пропала',"пропал",'потерялся','Потерялась', "убежал", "Убежала", "сбежал", "сбежала"]
        self.pattern = re.compile('|'.join(drop_words), re.IGNORECASE)
        self.df = df
        
        cities = np.unique(df['location'])
        self.cities = [str(city.strip()).lower() for city in cities]
        self._preprocess_data()
        if vectorizer is None:
            self.vectorizer = TfidfVectorizer()
        else:
            self.vectorizer = vectorizer
        self.tfidf_matrix = self._create_tfidf_matrix()

    def _preprocess_data(self):
        nltk.download('stopwords')
        stop_words = set(stopwords.words('russian'))
        def preprocess_text(text):
            tokens = word_tokenize(text.lower())
            tokens = [t for t in tokens if t not in stop_words]
            return ' '.join(tokens)
        self.df['title'] = self.df['title'].apply(preprocess_text)
        self.df['description'] = self.df['description'].apply(preprocess_text)

    def _create_tfidf_matrix(self):
        return self.vectorizer.fit_transform(self.df['title'] + ' ' + self.df['description'])

    def search_pet(self, query,type_search, top_n=30):
        query_tfidf = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_tfidf, self.tfidf_matrix).flatten()
        indices = similarities.argsort()[:-top_n-1:-1]
        data_ret = self.df.iloc[indices]
        if type_search == 'f':
            data_ret = data_ret[~data_ret['title'].apply(lambda x: bool(self.pattern.search(x))) & ~data_ret['description'].apply(lambda x: bool(self.pattern.search(x)))]
        city = None
        for word in query.split():
            if word.lower() in self.cities:
                city = word
                break

        if city:
            data_ret = data_ret[data_ret['location'].str.contains(city, case=False)]
        return data_ret


