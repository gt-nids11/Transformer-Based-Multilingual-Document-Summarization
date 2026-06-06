import os
import re
import torch
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Windows OpenMP duplicate initialization crash override
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

MODEL_NAME = "csebuetnlp/mT5_multilingual_XLSum"

def get_device():
    """Returns CUDA device if available, else CPU."""
    return "cuda" if torch.cuda.is_available() else "cpu"

@st.cache_resource
def load_model_and_tokenizer():
    """
    Loads and caches the tokenizer and model for csebuetnlp/mT5_multilingual_XLSum.
    Uses @st.cache_resource to load only once across page interactions.
    """
    device = get_device()
    print(f"Loading mT5 Multilingual XLSum model on {device}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME).to(device)
    print("Model loaded successfully.")
    return tokenizer, model

def segment_sentences(text):
    """
    Splits text into sentences in a language-agnostic way.
    Splits on English (. ? !) and Indic sentence enders (। ॥).
    """
    if not text:
        return []
    # Regex split pattern: splits on whitespace preceded by sentence punctuation
    sentence_end_pattern = r'(?<=[.!?।॥])\s+'
    sentences = re.split(sentence_end_pattern, text)
    return [s.strip() for s in sentences if s.strip()]

def chunk_text(text, max_words=300):
    """
    Groups sentences into chunks of up to max_words to prevent context window overflows.
    """
    sentences = segment_sentences(text)
    chunks = []
    current_chunk = []
    current_word_count = 0
    
    for sentence in sentences:
        words = len(sentence.split())
        if words > max_words:
            # If a single sentence exceeds the chunk word limit, split it by words
            if current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_word_count = 0
            
            s_words = sentence.split()
            for i in range(0, len(s_words), max_words):
                chunks.append(" ".join(s_words[i:i + max_words]))
            continue
            
        if current_word_count + words > max_words:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_word_count = words
        else:
            current_chunk.append(sentence)
            current_word_count += words
            
    if current_chunk:
        chunks.append(" ".join(current_chunk))
        
    return chunks

def summarize_chunk(chunk_text, tokenizer, model, num_beams=1):
    """
    Performs abstractive summarization on a single text chunk.
    Uses greedy decoding (num_beams=1) by default for faster CPU inference.
    """
    device = get_device()
    words_count = len(chunk_text.split())
    if words_count < 10:
        return chunk_text  # Skip summarizing very small chunks
        
    # Dynamically estimate target lengths (approx. 25% of original words)
    target_words = max(10, int(words_count * 0.25))
    max_tokens = min(128, max(30, int(target_words * 1.5)))
    min_tokens = min(64, max(5, int(target_words * 0.8)))
    
    if min_tokens >= max_tokens:
        min_tokens = max(5, max_tokens - 10)
        
    inputs = tokenizer(chunk_text, truncation=True, max_length=512, return_tensors="pt").to(device)
    
    with torch.no_grad():
        summary_ids = model.generate(
            inputs["input_ids"],
            num_beams=num_beams,
            no_repeat_ngram_size=2,
            length_penalty=1.0,
            min_length=min_tokens,
            max_length=max_tokens,
            early_stopping=True
        )
        
    summary_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary_text.strip()

def generate_summary(text, num_beams=1):
    """
    Splits the document, generates summaries for chunks, and aggregates them.
    
    Parameters:
      text: The preprocessed text of the document.
      num_beams: Number of beams (1 for speed/CPU default, 4 for quality).
      
    Returns:
      str: The aggregated summary.
    """
    if not text or not text.strip():
        return ""
        
    tokenizer, model = load_model_and_tokenizer()
    chunks = chunk_text(text, max_words=300)
    summarized_chunks = []
    
    for chunk in chunks:
        summary_chunk = summarize_chunk(chunk, tokenizer, model, num_beams=num_beams)
        if summary_chunk:
            summarized_chunks.append(summary_chunk)
            
    final_summary = " ".join(summarized_chunks)
    # Clean up multiple whitespaces
    final_summary = re.sub(r'\s+', ' ', final_summary).strip()
    return final_summary
