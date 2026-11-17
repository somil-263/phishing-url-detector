# 🛡️ Real-Time Phishing & Malicious URL Detector

[![Live App](https://img.shields.io/badge/Streamlit-Live%20App-FF4B4B?logo=streamlit)](https://phishing-url-detector-by-somil.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Naive%20Bayes-orange)

An end-to-end NLP & Cybersecurity classification pipeline trained on **549,000+ URLs** to detect phishing and malicious web links in real time using Character N-Gram TF-IDF vectorization and probability-calibrated **Multinomial Naive Bayes**.

🔗 **Live Web Scanner:** [Phishing URL Detector](https://phishing-url-detector-by-somil.streamlit.app/)

---

## 📌 Key Engineering Highlights
- **Data Deduplication & Leakage Prevention:** Removed duplicate URLs across 549,346 raw records (~507K unique URLs) prior to a stratified 80/20 split so identical links never leaked between train and test sets.
- **Subword & Typosquatting Detection (`char_wb`):** Replaced word-level tokenization with **3–5 character n-grams** (`max_features=150,000`) to capture obfuscated brand spoofing (e.g., `paypa1`, `webscrcmd`, random hex tokens) that standard word tokenizers miss.
- **Lidstone Smoothing & Threshold Calibration:** Tuned Laplace/Lidstone smoothing (`alpha=0.01`) and lowered the decision threshold from `0.50` to **`0.40`** via `predict_proba()`, boosting malicious URL recall from **86% to 90%** while maintaining `96.21%` overall accuracy.

---

## 📊 Model Benchmarking (101,440 Test URLs)

| Model & Feature Setup | Test Accuracy | Malicious Recall | Malicious F1-Score |
| :--- | :---: | :---: | :---: |
| BernoulliNB (Word N-Grams) | `95.52%` | `0.85` | `0.90` |
| ComplementNB (Word N-Grams) | `95.69%` | `0.89` | `0.91` |
| MultinomialNB (Word N-Grams) | `95.98%` | `0.86` | `0.91` |
| **MultinomialNB (`char_wb` 3–5, `alpha=0.01`, `t=0.40`)** | **`96.21%`** | **`0.90`** | **`0.91`** |

---

## ⚠️ Known Limitations & Production Scope
- **Keyword Bias:** Utility terms frequently abused in malware campaigns (e.g., `pdf`, `converter`, `free`) can elevate risk scores on legitimate tools due to training dataset distribution; production deployments pair this model with domain-age/WHOIS and SSL reputation signals.

---

## 📂 Repository Structure
```text
├── notebook.ipynb               # EDA, deduplication, NB variants benchmarking & threshold tuning
├── streamlit_app.py             # Real-time Streamlit URL scanning application
├── phishing_url_model.joblib    # Compressed TF-IDF char vectorizer, MultinomialNB & optimal threshold
├── requirements.txt             # Python dependencies
└── README.md                    # Documentation
