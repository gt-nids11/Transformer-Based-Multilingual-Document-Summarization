# Transformer-Based Multilingual Document Summarization

A beginner-friendly Natural Language Processing (NLP) application that accepts a PDF or TXT document and generates a concise summary in the same language. The application automatically detects the document language and utilizes a pre-trained **mT5** transformer model for abstractive text summarization.

---

## 🚀 Key Features

* **Multi-Format Extraction**: Parses PDF text using `pypdf` and text documents using standard encoders.
* **Auto Language Detection**: Uses `langdetect` to identify document language out of 10+ languages (English, Hindi, Marathi, Bengali, Tamil, etc.).
* **Language Preservation**: Auto-generates the summary in the detected document language (e.g. Hindi document yields a Hindi summary).
* **Abstractive Summarization**: Utilizes the pre-trained `csebuetnlp/mT5_multilingual_XLSum` transformer model to rewrite summaries.
* **Streamlit Dashboard**: Soft dark theme with shadows, highlights, metric cards, and responsive previews.
* **Performance Caching**: Employs Streamlit's `@st.cache_resource` to ensure the summarizer model is loaded only once.
* **Robust Error Handling**: Handles corrupted PDFs, empty uploads, and low-word count constraints gracefully.

---

## 📂 Project Directory Structure

```text
multilingual-document-summarizer/
├── app.py              # Streamlit UI & Orchestration Logic
├── summarizer.py       # Model Loader, Chunking & mT5 inference
├── utils.py            # PDF/TXT Parsers, Language Detectors & Stats
├── requirements.txt    # Dependency lists
└── README.md           # Documentation
```

---

## ⚙️ Installation & Setup

### Step 1: Open Project Directory
Navigate to the project directory:
```bash
cd c:\Users\Asus\OneDrive\Desktop\nlpSummarizer
```

### Step 2: Set Up Virtual Environment (Optional but Recommended)
Create and activate a virtual environment to isolate the project packages:
```powershell
python -m venv venv
# On Windows:
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Required Dependencies
Install the required standard libraries from `requirements.txt`:
```powershell
pip install -r requirements.txt
```

### Step 4: Run the Application
Start the Streamlit web dashboard:
```bash
streamlit run app.py
```
A browser tab will automatically open at `http://localhost:8501`.

---

## 📖 How to Use

1. **Upload File**: Drag and drop a `.pdf` or `.txt` document into the upload pane.
2. **View Info**: The app will extract the text, detect its language, and display statistics (Character and Word Counts).
3. **Preview**: View the scrollable container showing the first 1000 characters of the document.
4. **Generate Summary**: Click the primary `🚀 Generate Summary` button. A loading spinner will appear while the mT5 model processes the text, displaying the summary inside a styled green container.
