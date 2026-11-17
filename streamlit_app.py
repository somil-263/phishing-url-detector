import re
import streamlit as st
import joblib
from urllib.parse import urlparse

st.set_page_config(page_title="Phishing URL Scanner", page_icon="🛡️", layout="centered")

@st.cache_resource
def load_bundle():
    return joblib.load("phishing_url_model.joblib")

bundle = load_bundle()
vectorizer = bundle["vectorizer"]
model = bundle["model"]
threshold = bundle["threshold"]

TRUSTED_DOMAINS = {
    "google.com", "youtube.com", "github.com", "linkedin.com", "microsoft.com",
    "apple.com", "amazon.com", "amazon.in", "ilovepdf.com", "wikipedia.org",
    "kaggle.com", "streamlit.app", "huggingface.co", "stackoverflow.com",
    "claude.ai", "openai.com", "chatgpt.com", "anthropic.com"
}

UUID_PATTERN = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.IGNORECASE
)

def parse_and_clean(raw_url: str):
    u = raw_url.strip().lower()
    parsed = urlparse(u if "://" in u else "http://" + u)
    host = parsed.netloc.split(":")[0]
    if host.startswith("www."):
        host = host[4:]
    # Remove random UUID session/chat IDs so char n-grams don't flag modern SaaS links
    clean_path = UUID_PATTERN.sub("", parsed.path)
    clean_for_model = (host + clean_path).rstrip("/")
    return host, clean_for_model

st.title("🛡️ Real-Time Phishing URL Detector")
st.write(
    "Hybrid URL scanner combining domain verification, UUID normalization, and Character N-Gram TF-IDF "
    "with tuned Multinomial Naive Bayes (`96.21%` Accuracy, `90%` Malicious Recall)."
)

url_input = st.text_input(
    "Enter a website URL to scan:",
    value="www.dghjdgf.com/paypal.co.uk/cycgi-bin/webscrcmd"
)

if st.button("Scan URL", type="primary"):
    if not url_input.strip():
        st.warning("Please enter a valid URL first.")
    else:
        host, clean_url = parse_and_clean(url_input)

        if host in TRUSTED_DOMAINS:
            st.metric(label="Phishing Risk Probability", value="0.00%")
            st.success(f"✅ SAFE / VERIFIED DOMAIN (`{host}`)")
        else:
            url_vec = vectorizer.transform([clean_url])
            bad_idx = list(model.classes_).index(1)
            phishing_prob = float(model.predict_proba(url_vec)[0][bad_idx])

            st.metric(label="Phishing Risk Probability", value=f"{phishing_prob * 100:.2f}%")

            if phishing_prob >= threshold:
                st.error(f"🚨 PHISHING / MALICIOUS URL DETECTED (Risk ≥ {threshold * 100:.0f}% threshold)")
            else:
                st.success("✅ SAFE / LEGITIMATE URL")
