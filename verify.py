import numpy as np
import tensorflow as tf
import pickle
from keras.preprocessing.text import one_hot
from keras.preprocessing.sequence import pad_sequences
from nltk.tokenize import word_tokenize
from keras.preprocessing.text import Tokenizer
# from sklearn.feature_extraction.text import TfidfVectorizer

interpreter = tf.lite.Interpreter(model_path="./models/model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_shape = input_details[0]['shape']

vectorizer = pickle.load(open('./models/vectorizer.pickle', 'rb'))

def verify(data):
    x = vectorizer.transform(data).toarray() #vectorizer.text_to_sequences(data)   #
    input_data = np.array(x[0], dtype=np.float32).reshape(1,17510)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    return output_data[0][0]

