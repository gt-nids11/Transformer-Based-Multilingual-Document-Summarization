import os
import sys

# Configure stdout to handle UTF-8 encoding for Indic scripts on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from utils import extract_text, detect_document_language, get_document_stats

def run_tests():
    print("=" * 65)
    print("🧪 Testing Simplified Multilingual NLP Pipeline Utility Logic")
    print("=" * 65)
    
    # 1. Test Language Detection
    print("\n--- Testing Language Detection ---")
    test_cases = [
        ("This is a simple English sentence for NLP testing.", "en", "English"),
        ("यह एक हिंदी वाक्य है जिसका उपयोग हम भाषा पहचान के लिए कर रहे हैं।", "hi", "Hindi"),
        ("हा एक मराठी वाक्य आहे ज्याचा वापर आम्ही चाचणीसाठी करत आहोत.", "mr", "Marathi"),
        ("આ એક ગુજરાતી વાક્ય છે જેનો ઉપયોગ અમે ભાષા ચકાસણી માટે કરી રહ્યા છીએ.", "gu", "Gujarati"),
    ]
    
    for text, expected_code, expected_name in test_cases:
        code, name = detect_document_language(text)
        print(f"Input: '{text[:25]}...' -> Detected: {name} ({code})")
        assert code == expected_code, f"Failed language detection for {expected_code}"
    print("[OK] Language Detection: ALL PASSED")
    
    # 2. Test Document Stats
    print("\n--- Testing Document Stats ---")
    sample_text = "Word1 Word2 Word3 Word4 Word5"
    stats = get_document_stats(sample_text)
    print(f"Stats computed: {stats}")
    assert stats['words'] == 5, "Word count mismatch."
    assert stats['characters'] == len(sample_text), "Character count mismatch."
    print("[OK] Document Statistics: PASSED")
    
    # 3. Test Text File Extraction
    print("\n--- Testing Document Reader (TXT) ---")
    dummy_txt_path = "dummy_test_doc.txt"
    dummy_content = "This is a dummy document for unit testing the pypdf/txt document reader module.\nIt has multiple lines."
    with open(dummy_txt_path, "w", encoding="utf-8") as f:
        f.write(dummy_content)
        
    try:
        extracted = extract_text(dummy_txt_path, dummy_txt_path)
        print(f"Extracted content:\n{extracted}")
        assert dummy_content.strip() in extracted.strip(), "Extracted text does not match written text."
        print("[OK] TXT Document Reader: PASSED")
    finally:
        if os.path.exists(dummy_txt_path):
            os.remove(dummy_txt_path)
            
    print("\n" + "=" * 65)
    print("[SUCCESS] ALL NLP UTILITY MODULES LOGIC PASSED SUCCESSFULLY!")
    print("=" * 65)

if __name__ == "__main__":
    run_tests()
