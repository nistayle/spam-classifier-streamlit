import streamlit as st
import joblib
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

# Download stopwords kalo belum
nltk.download('stopwords')

# Load model dan vectorizer
model = joblib.load('spam_classifier_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

# Inisialisasi stopwords & stemmer
stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

# Preprocessing function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z]', ' ', text)
    words = text.split()
    words = [ps.stem(word) for word in words if word not in stop_words]
    return ' '.join(words)

# Streamlit App Layout
st.title("📩 Spam Classifier AI")

input_text = st.text_area("Masukkan pesan teks di sini:")

if st.button("Prediksi"):
    if input_text:
        clean_text = preprocess_text(input_text)
        vectorized_text = vectorizer.transform([clean_text])
        prediction = model.predict(vectorized_text)
        result = "📢 SPAM!" if prediction[0] == 1 else "✅ HAM (Bukan spam)"
        st.subheader("Hasil:")
        st.success(result)
    else:
        st.warning("Tolong isi dulu teksnya.")