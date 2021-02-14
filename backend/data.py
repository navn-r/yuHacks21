#  __  __            _     _              _                          _             
# |  \/  | __ _  ___| |__ (_)_ __   ___  | |    ___  __ _ _ __ _ __ (_)_ __   __ _ 
# | |\/| |/ _` |/ __| '_ \| | '_ \ / _ \ | |   / _ \/ _` | '__| '_ \| | '_ \ / _` |
# | |  | | (_| | (__| | | | | | | |  __/ | |__|  __/ (_| | |  | | | | | | | | (_| |
# |_|  |_|\__,_|\___|_| |_|_|_| |_|\___| |_____\___|\__,_|_|  |_| |_|_|_| |_|\__, |
#                                                                            |___/ 
# https://www.kaggle.com/clmentbisaillon/fake-and-real-news-dataset
import csv
import random
from numpy import array
from keras.preprocessing.text import one_hot
from keras.preprocessing.sequence import pad_sequences
from keras import layers
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.embeddings import Embedding
from keras.preprocessing.text import Tokenizer
from nltk.tokenize import word_tokenize
from tensorflow import lite
import tensorflow as tf
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing import sequence
from tensorflow.python.keras.layers.pooling import GlobalMaxPool1D
from keras.preprocessing.text import Tokenizer

MAX_SEQUENCE_LENGTH = 5000
MAX_NUM_WORDS = 25000
EMBEDDING_DIM = 300

physical_devices = tf.config.experimental.list_physical_devices('GPU')
assert len(physical_devices) > 0, "Not enough GPU hardware devices available"
config = tf.config.experimental.set_memory_growth(physical_devices[0], True)

def get_data():
    fake_articles = []
    real_articles = []
    with open("./data/Fake.csv") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            fake_articles.append(row)
    with open("./data/True.csv") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            real_articles.append(row)
    fake_articles.pop(0)
    real_articles.pop(0)
    fake_articles = [k[0] for k in fake_articles]
    real_articles = [k[0] for k in real_articles]
    fake_val = [0 for k in fake_articles]
    real_val = [1 for k in real_articles]
    
    return fake_articles + real_articles, fake_val + real_val

def find_unique(corpus):
    all_words = []
    for sent in corpus:
        tokenize_word = word_tokenize(sent)
        for word in tokenize_word:
            all_words.append(word)
    unique_words = set(all_words)
    return len(unique_words)

corpus, values = get_data()
c = list(zip(corpus, values))
random.shuffle(c)
corpus, values = zip(*c)
values = array(values)

vectorizer = TfidfVectorizer(stop_words="english") #Tokenizer() 
# vectorizer.fit_on_texts(corpus)
# sequences = vectorizer.texts_to_sequences(corpus)
# word_index = vectorizer.word_index
# num_words = min(MAX_NUM_WORDS, len(word_index)) + 1
# data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH, padding='pre', truncating='pre')

X_train, X_test, y_train, y_test = train_test_split(corpus, values, test_size=0.4, random_state=42)
# X_train = [np.array(k) for k in X_train]
# X_test = [np.array(k) for k in X_test]

vectorizer.fit(X_train)
corpus_vectorized = vectorizer.transform(X_train).toarray()
X_train = vectorizer.transform(X_train).toarray()
X_test = vectorizer.transform(X_test).toarray()

pickle.dump(vectorizer, open('vectorizer.pickle', 'wb'))

vocab_length = max([len(k.split(' ')) for k in corpus])
model = Sequential()
# model = Sequential([
#     layers.Embedding(num_words, EMBEDDING_DIM, input_length=MAX_SEQUENCE_LENGTH, trainable=True),
#     layers.Conv1D(128, 5, activation='relu'),
#     layers.GlobalMaxPooling1D(),
#     layers.Dense(128, activation='relu'),
#     layers.Dense(1, activation='sigmoid')
#     ])

model.add(Dense(128, input_dim=len(corpus_vectorized[0]), activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.add(Flatten())
model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
print(model.summary())
model.fit(X_train, y_train, epochs=25, verbose=1)
model.save("fake_news_model1")
Converter = lite.TFLiteConverter.from_keras_model(model)
TFLiteModel = Converter.convert()
open("test_model.tflite", "wb").write(TFLiteModel)
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print('Accuracy: %f' % (accuracy*100))
