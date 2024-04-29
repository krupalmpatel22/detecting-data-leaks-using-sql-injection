from sklearn.model_selection import train_test_split
from tensorflow.keras import models
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd
import os

def predict_sql_injection(text):
    file_path = os.path.dirname(os.path.abspath(__file__))
    data_file_path = file_path + "\data\sqliv2.csv"
    model_path = file_path + "\SQLi.h5"
    # data_file_path = os.getcwd() +"\data\sqliv2.csv"
    # model_path = os.getcwd() +"\SQLi.h5"
    df = pd.read_csv(data_file_path, encoding='utf-16')
    df['Sentence'] = df['Sentence'].astype(str)

    # Example dataset (in practice, use a larger, more diverse dataset)
    strings = df['Sentence'].to_list()  # Not SQL injection prone
    labels = df['Label'].to_list()

    X_train, X_test, y_train, y_test = train_test_split(strings, labels, test_size=0.2, random_state=42)

    # Tokenize the strings
    tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
    tokenizer.fit_on_texts(X_train)

    model = models.load_model(model_path)
    sequence = tokenizer.texts_to_sequences([text])

    padded = pad_sequences(sequence, maxlen=100, padding='post')
    prediction = model.predict(padded)
    print(prediction[0][0])
    return prediction[0][0] > 0.8  # Returns True if SQL injection prone, False otherwise

def get_model():
    file_path = os.path.dirname(os.path.abspath(__file__))
    print(file_path)
    data_file_path = file_path + "/data/sqliv2.csv"
    model_path = file_path + "/SQLi.h5"
    # data_file_path = os.getcwd() +"\data\sqliv2.csv"
    # model_path = os.getcwd() +"\SQLi.h5"
    df = pd.read_csv(data_file_path, encoding='utf-16')
    df['Sentence'] = df['Sentence'].astype(str)

    # Example dataset (in practice, use a larger, more diverse dataset)
    strings = df['Sentence'].to_list()  # Not SQL injection prone
    labels = df['Label'].to_list()

    X_train, X_test, y_train, y_test = train_test_split(strings, labels, test_size=0.2, random_state=42)

    # Tokenize the strings
    tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
    tokenizer.fit_on_texts(X_train)

    model = models.load_model(model_path)

    return model, tokenizer

if __name__ == "__main__":
    text = "' ;DROP TABLE users; --"
    print(predict_sql_injection(text))