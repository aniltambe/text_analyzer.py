import re
from collections import Counter

def clean_text(text):
    text = re.sub(r'\[[0-9]*\]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def calculate_word_frequencies(formatted_text):
    stopwords = ["the", "a", "an", "and", "but", "if", "or", "because", "as", "what", 
                 "which", "this", "that", "these", "those", "then", "just", "so", "than",
                 "to", "for", "with", "about", "against", "between", "into", "through",
                 "is", "am", "are", "was", "were", "be", "been", "being", "have", "has", "had"]
    words = re.findall(r'\b[a-zA-Z]{3,}\b', formatted_text.lower())
    frequencies = Counter([word for word in words if word not in stopwords])
    return frequencies

def generate_summary(text, top_sentences_count=3):
    cleaned = clean_text(text)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    if len(sentences) <= top_sentences_count:
        return text
    frequencies = calculate_word_frequencies(cleaned)
    max_freq = max(frequencies.values()) if frequencies else 1
    for word in frequencies:
        frequencies[word] = (frequencies[word] / max_freq)
    sentence_scores = {}
    for sent in sentences:
        for word in re.findall(r'\b[a-zA-Z]{3,}\b', sent.lower()):
            if word in frequencies:
                if sent not in sentence_scores:
                    sentence_scores[sent] = frequencies[word]
                else:
                    sentence_scores[sent] += frequencies[word]
    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:top_sentences_count]
    return " ".join(summary_sentences)

if __name__ == "__main__":
    print("=== Text Summarizer & Keyword Extractor ===")
    print("Enter or paste your text below (Press Enter then Ctrl+D or Ctrl+Z to finish):")
    lines = []
    while True:
        try:
            line = input()
            lines.append(line)
        except EOFError:
            break
    user_text = "\n".join(lines).strip()
    if len(user_text) < 100:
        print("\nError: Please enter a longer text to analyze (minimum 100 characters).")
    else:
        print("\n--- Generating Summary ---")
        print(generate_summary(user_text, 3))
        print("\n--- Extracting Top Keywords ---")
        top_keywords = calculate_word_frequencies(clean_text(user_text)).most_common(5)
        for keyword, count in top_keywords:
            print(f"- {keyword}: {count} times")
