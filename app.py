from flask import Flask, render_template, jsonify
import speech_recognition as sr
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter

app = Flask(__name__)

# Path to your Excel file
word_list_path = r"D:\py\audio\Copy of Positive and Negative Word List.xlsx"

# Load words
def load_word_list(path):
    try:
        df = pd.read_excel(path, sheet_name='Sheet1')
        positive_words = set(df['Positive Sense Word List'].dropna().str.lower().tolist())
        negative_words = set(df['Negative Sense Word List'].dropna().str.lower().tolist())
        return positive_words, negative_words
    except Exception as e:
        print(f"Error loading word list: {e}")
        return set(), set()

positive_words, negative_words = load_word_list(word_list_path)

# Analyze sentence
def analyze_sentence(sentence, positive_words, negative_words):
    words = word_tokenize(sentence.lower())
    word_counts = Counter(words)

    pos_list = []
    neg_list = []

    for word in words:
        if word in positive_words:
            pos_list.append(word)
        elif word in negative_words:
            neg_list.append(word)

    positive_count = len(pos_list)
    negative_count = len(neg_list)

    return positive_count, negative_count, pos_list, neg_list

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio, language='en-IN')  # You can change the language
            print(f"Recognized: {text}")

            positive_count, negative_count, pos_list, neg_list = analyze_sentence(text, positive_words, negative_words)

            classification = "Positive Sentence" if positive_count >= negative_count else "Negative Sentence"

            return jsonify({
                'sentence': text,
                'classification': classification,
                'positive_words': pos_list,
                'negative_words': neg_list
            })

    except sr.WaitTimeoutError:
        return jsonify({'error': 'Listening timed out. Please try speaking again.'})
    except sr.UnknownValueError:
        return jsonify({'error': 'Could not understand audio.'})
    except sr.RequestError:
        return jsonify({'error': 'Could not request results. Check internet connection.'})
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {e}'})

if __name__ == '__main__':
    app.run(debug=True)
