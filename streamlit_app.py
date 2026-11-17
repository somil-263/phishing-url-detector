import streamlit as st
import joblib

st.set_page_config(page_title="Phishing URL Scanner", page_icon="🛡️", layout="centered")

@st.cache_resource
def load_bundle():
    return joblib.load("phishing_url_model.joblib")

bundle = load_bundle()
vectorizer = bundle["vectorizer"]
model = bundle["model"]
threshold = bundle["threshold"]

st.title("🛡️ Real-Time Phishing URL Detector")
st.write(
    "Detects malicious and phishing URLs using Character N-Gram TF-IDF (3–5 chars) "
    "and tuned Multinomial Naive Bayes (`96.21%` Accuracy, `0.91` Phishing F1-Score)."
)

url_input = st.text_input(
    "Enter a website URL to scan:",
    value="www.dghjdgf.com/paypal.co.uk/cycgi-bin/webscrcmd"
)

if st.button("Scan URL", type="primary"):
    if not url_input.strip():
        st.warning("Please enter a valid URL first.")
    else:
        url_vec = vectorizer.transform([url_input.strip()])
        bad_idx = list(model.classes_).index(1)
        phishing_prob = float(model.predict_proba(url_vec)[0][bad_idx])

        st.metric(label="Phishing Risk Probability", value=f"{phishing_prob * 100:.2f}%")

        if phishing_prob >= threshold:
            st.error(f"🚨 PHISHING / MALICIOUS URL DETECTED (Risk ≥ {threshold * 100:.0f}% threshold)")
        else:
            st.success("✅ SAFE / LEGITIMATE URL")
