import sys
import warnings
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QSizePolicy
from functools import partial
import nltk
import random
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet, stopwords
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

warnings.filterwarnings("ignore", category=DeprecationWarning)

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

def get_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonym = lemma.name().replace("_", " ").replace("-", " ").lower()
            synonym = "".join([char for char in synonym if char.isalnum()])
            synonyms.append(synonym)
    return synonyms

def semantic_similarity(word1, word2):
    word1_synonyms = set(get_synonyms(word1))
    word2_synonyms = set(get_synonyms(word2))
    if not word1_synonyms or not word2_synonyms:
        return 0
    similarity = len(word1_synonyms.intersection(word2_synonyms)) / (len(word1_synonyms.union(word2_synonyms)) or 1)
    return similarity

def paraphrase_sentence(sentence):
    words = word_tokenize(sentence)
    paraphrased_words = []
    for word in words:
        if word.lower() not in stop_words:  
            synonyms = get_synonyms(word)
            if synonyms:
                synonyms.sort(key=lambda x: semantic_similarity(x, word), reverse=True)
                paraphrased_words.append(synonyms[0])
            else:
                paraphrased_words.append(word)
        else:
            paraphrased_words.append(word)
    return ' '.join(paraphrased_words)

def rephrase_paragraph(text):
    sentences = sent_tokenize(text)
    return ' '.join([paraphrase_sentence(sentence) for sentence in sentences])

def summarize_paragraph_text_rank(paragraph, num_sentences=3):
    try:
        summarizer = TextRankSummarizer()
        parser = PlaintextParser.from_string(paragraph, Tokenizer("english"))
        summary = summarizer(parser.document, num_sentences)
        return "\n".join(str(sentence) for sentence in summary)
    except Exception as e:
        return f"Error occurred during summarization: {str(e)}"

def generate_points(paragraph):
    words = word_tokenize(paragraph)
    words = [word for word in words if word.lower() not in stop_words]  
    fdist = nltk.FreqDist(words)
    keyword_list = [word for word, _ in fdist.most_common(5)]
    points = []
    sentences = sent_tokenize(paragraph)
    for i, sentence in enumerate(sentences, start=1):
        words = word_tokenize(sentence)
        common_keywords = set(words) & set(keyword_list)
        if common_keywords:
            paraphrased_sentence = paraphrase_sentence(sentence)
            points.append(f"{i}. {paraphrased_sentence}")  
    return points

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Text Processing Tool")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.input_label = QLabel("Enter your text:")
        self.layout.addWidget(self.input_label)

        self.input_text = QTextEdit()
        self.input_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.input_text)

        self.options_layout = QHBoxLayout()
        self.layout.addLayout(self.options_layout)

        self.button_rephrase = QPushButton("Rephrase")
        self.button_rephrase.clicked.connect(self.rephrase)
        self.options_layout.addWidget(self.button_rephrase)

        self.button_summarize = QPushButton("Summarize")
        self.button_summarize.clicked.connect(self.summarize)
        self.options_layout.addWidget(self.button_summarize)

        self.button_points = QPushButton("Important Points")
        self.button_points.clicked.connect(self.show_points)
        self.options_layout.addWidget(self.button_points)

        self.output_label = QLabel("Output:")
        self.layout.addWidget(self.output_label)

        self.output_text = QTextEdit()
        self.output_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.output_text)

    def rephrase(self):
        input_text = self.input_text.toPlainText()
        output_text = rephrase_paragraph(input_text)
        self.output_text.setPlainText(output_text)

    def summarize(self):
        input_text = self.input_text.toPlainText()
        output_text = summarize_paragraph_text_rank(input_text)
        self.output_text.setPlainText(output_text)

    def show_points(self):
        input_text = self.input_text.toPlainText()
        output_text = "\n".join(generate_points(input_text))
        self.output_text.setPlainText(output_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
