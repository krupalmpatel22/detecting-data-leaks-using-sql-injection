from sklearn.model_selection import train_test_split
from tensorflow.keras import models
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd

def predict_sql_injection(text):
    df = pd.read_csv('D:\[0] PERSONAL\SQLi\model\data\sqliv2.csv', encoding='utf-16')
    df['Sentence'] = df['Sentence'].astype(str)

    # Example dataset (in practice, use a larger, more diverse dataset)
    strings = df['Sentence'].to_list()  # Not SQL injection prone
    labels = df['Label'].to_list()

    X_train, X_test, y_train, y_test = train_test_split(strings, labels, test_size=0.2, random_state=42)

    # Tokenize the strings
    tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
    tokenizer.fit_on_texts(X_train)

    model =  models.load_model('D:\[0] PERSONAL\SQLi\model\SQLi.h5')
    sequence = tokenizer.texts_to_sequences([text])

    padded = pad_sequences(sequence, maxlen=100, padding='post')
    prediction = model.predict(padded)

    return prediction[0][0] > 0.8  # Returns True if SQL injection prone, False otherwise


if __name__ == "__main__":
    text = "UID = '' OR 1=1--"
    print(predict_sql_injection(text))