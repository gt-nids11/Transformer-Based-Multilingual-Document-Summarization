import os
import pypdf
from langdetect import detect, DetectorFactory

# Enforce deterministic results for language detection
DetectorFactory.seed = 0

# Mapping of langdetect codes to user-friendly display names
LANGUAGE_MAP = {
    'en': 'English',
    'hi': 'Hindi',
    'mr': 'Marathi',
    'bn': 'Bengali',
    'ta': 'Tamil',
    'gu': 'Gujarati',
    'te': 'Telugu',
    'kn': 'Kannada',
    'ml': 'Malayalam',
    'pa': 'Punjabi',
    'ur': 'Urdu'
}

def validate_file(filename):
    """
    Validates if the file format is supported (.pdf or .txt).
    """
    ext = os.path.splitext(filename)[1].lower()
    return ext in ['.pdf', '.txt']

def extract_text_from_pdf(file_source):
    """
    Extracts text from all readable pages of a PDF file using pypdf.
    Handles file path (str) or file-like object (BytesIO).
    """
    try:
        reader = pypdf.PdfReader(file_source)
        text_list = []
        for page_idx, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text_list.append(page_text)
        
        extracted_text = "\n".join(text_list)
        return extracted_text
    except Exception as e:
        raise RuntimeError(f"PyPDF failed to parse document: {e}")

def extract_text_from_txt(file_source):
    """
    Reads and decodes text from a TXT file source, trying multiple encodings.
    Handles file path (str) or file-like object.
    """
    if isinstance(file_source, str):
        # File path
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'utf-16']
        for encoding in encodings:
            try:
                with open(file_source, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        raise RuntimeError("Failed to decode text file with standard encodings.")
    else:
        # File-like object from Streamlit (BytesIO or StringIO)
        try:
            content = file_source.read()
            # If it's BytesIO, decode it
            if isinstance(content, bytes):
                encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'utf-16']
                for encoding in encodings:
                    try:
                        return content.decode(encoding)
                    except UnicodeDecodeError:
                        continue
                raise RuntimeError("Failed to decode byte stream.")
            else:
                # Already a string (StringIO)
                return content
        except AttributeError:
            return file_source.read()

def extract_text(file_source, filename):
    """
    Orchestrates text extraction based on file extension.
    """
    if not validate_file(filename):
        raise ValueError("Unsupported file format. Please upload a PDF or TXT file.")
        
    ext = os.path.splitext(filename)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(file_source)
    elif ext == '.txt':
        return extract_text_from_txt(file_source)
    else:
        raise ValueError(f"Unhandled file extension: {ext}")

def detect_document_language(text):
    """
    Detects the language of the document using langdetect.
    Returns:
        tuple: (language_code, name)
    """
    if not text or not text.strip():
        return 'en', 'English'
        
    try:
        # Sample first 1000 characters for speed and robustness
        sample = text[:1000]
        code = detect(sample)
        name = LANGUAGE_MAP.get(code, f"Other ({code})")
        return code, name
    except Exception as e:
        # Fallback to English on error
        print(f"Language detection exception: {e}")
        return 'en', 'English'

def get_document_stats(text):
    """
    Computes text statistics: character count and word count.
    """
    char_count = len(text)
    word_count = len(text.split())
    return {
        'characters': char_count,
        'words': word_count
    }
