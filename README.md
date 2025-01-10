
# Streamlit Sentiment Analysis Frontend

This project is a Streamlit-based frontend for visualizing sentiment analysis results. It communicates with a FastAPI backend to upload conversation transcripts and display sentence-level sentiment analysis, speaker comparisons, and drastic sentiment shifts.

---

## Features
- **Interactive File Upload:** Upload conversation transcripts in `.txt` format.
- **Visualization:** Display sentence-level sentiment scores, polarity, and intensity using interactive graphs.
- **Speaker-Specific Analysis:** Compare sentiments between speakers.
- **Drastic Sentiment Shifts:** Highlight sentences causing major sentiment changes.

---

## Requirements
- Python 3.8 or higher
- `pip` for Python package management

---

## Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/srijan960/sentiment-analysis-frontend.git
cd sentiment-analysis-frontend
```

**2. Install Dependencies**

  

Install the required Python packages listed in the requirements.txt file.

```bash
pip install -r requirements.txt
```

**3. Update Backend URL**

  

Edit the BACKEND_URL variable in the main.py file to point to your FastAPI backend (e.g., http://127.0.0.1:8000/upload).

**Running the App**

  

Run the following command to start the Streamlit app:

```bash
streamlit run main.py
```
Streamlit will launch the app in your default web browser. You can also access it at http://localhost:8501.

