# General Purpose Chatbot System

Repository for Rule-based NLP Chatbot System project written using Python.

## Steps For Running

Make sure the following modules are installed before running: pandas, bs4, nltk and scikit-learn. They can be installed using either conda or pip. To ensure all the required parts of nltk are downloaded, use nltk.download('all').

Ensure no files are renamed, and that the directory structure is maintained as the following:

```
src
│
├── datasets
│   ├── COMP3074-CW1-Dataset.csv
│   └── Intents.json
├── output
│   ├── Dataset.json
│   ├── tfidf_matrix.joblib
│   └── tfidf_vectorizer.joblib
├── chatbot.py
├── intent.py
├── process.py
├── retrieval.py
├── talk.py
└── transaction.py
```

The program can be run using the following command: python chatbot.py
