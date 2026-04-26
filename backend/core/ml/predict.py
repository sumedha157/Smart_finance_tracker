import pickle
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = pickle.load(open(os.path.join(BASE_DIR, "model.pkl"), "rb"))
vectorizer = pickle.load(open(os.path.join(BASE_DIR, "vectorizer.pkl"), "rb"))

def predict_category(text):
    text = text.lower()
    X = vectorizer.transform([text])

    pred = model.predict(X)[0]
    prob = model.predict_proba(X).max()

    return pred, prob