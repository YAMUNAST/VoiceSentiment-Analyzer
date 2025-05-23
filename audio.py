import pandas as pd
import re
from collections import Counter
import speech_recognition as sr
import nltk
from nltk.tokenize import word_tokenize

# Ensure nltk resources are downloaded (uncomment if needed)
# nltk.download('punkt')

# Path for the Excel file
word_list_path = r"D:\py\audio\Copy of Positive and Negative Word List.xlsx"

def load_word_list(path):
    """Load positive and negative words from an Excel file."""
    try:
        df = pd.read_excel(path, sheet_name='Sheet1')
        positive_words = set(df['Positive Sense Word List'].dropna().str.lower().tolist())
        negative_words = set(df['Negative Sense Word List'].dropna().str.lower().tolist())
        return positive_words, negative_words
    except Exception as e:
        print(f"Error loading word list: {e}")
        return set(), set()

def analyze_sentence(sentence, positive_words, negative_words):
    """Analyze a single sentence for positive and negative word counts and lists."""
    words = word_tokenize(sentence.lower())
    word_counts = Counter(words)

    positive_found = []
    negative_found = []

    for word, count in word_counts.items():
        clean_word = word.lower()
        if clean_word in positive_words:
            positive_found.extend([clean_word] * count)
        elif clean_word in negative_words:
            negative_found.extend([clean_word] * count)

    positive_count = len(positive_found)
    negative_count = len(negative_found)

    return positive_count, negative_count, word_counts, positive_found, negative_found

def summarize_analysis(word_counts, positive_count, negative_count, positive_found, negative_found):
    """Generate a summary of the analysis results."""
    total_words = sum(word_counts.values())
    summary = {
        "Total words": total_words,
        "Positive words count": positive_count,
        "Negative words count": negative_count,
        "Positive words found": positive_found,
        "Negative words found": negative_found,
        "Overall word counts": dict(word_counts)
    }
    return summary

def display_summary(summary, sentence_type):
    """Display the analysis results in a formatted way."""
    print("\n--- Analysis Results ---")
    for key, value in summary.items():
        print(f"{key}: {value}")
    print(f"The sentence is classified as: {sentence_type}.")

def get_user_input():
    """Capture audio input from the user using the microphone."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say a sentence (you have 30 seconds):")
        
        # Adjust the listen parameters for longer input
        audio = recognizer.listen(source, timeout=None, phrase_time_limit=30)

        try:
            # Recognize speech using Google Web Speech API
            user_input = recognizer.recognize_google(audio)
            print(f"\nYou said: {user_input}")
            return user_input
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from the speech recognition service; {e}")
            return None

def determine_stress_level(positive_count, negative_count):
    """Determine if the sentence is positive or negative based on word counts."""
    return "Negative Sentence" if negative_count > positive_count else "Positive Sentence"

def main():
    """Main function to execute the sentiment analysis."""
    positive_words, negative_words = load_word_list(word_list_path)
    user_input = get_user_input()

    if user_input:
        positive_count, negative_count, word_counts, positive_found, negative_found = analyze_sentence(
            user_input, positive_words, negative_words)

        sentence_type = determine_stress_level(positive_count, negative_count)

        summary = summarize_analysis(word_counts, positive_count, negative_count, positive_found, negative_found)
        display_summary(summary, sentence_type)

if __name__ == "__main__":
    main()
