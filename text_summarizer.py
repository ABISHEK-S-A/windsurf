import sys
import spacy
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QPushButton, 
                           QVBoxLayout, QWidget, QFileDialog, QLabel, QSpinBox)
from PyQt5.QtCore import Qt
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

class TextSummarizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
        # Download required NLTK data
        nltk.download('punkt')
        nltk.download('stopwords')
        
    def initUI(self):
        self.setWindowTitle('Text Summarizer')
        self.setGeometry(100, 100, 800, 600)
        
        # Main widget and layout
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)
        
        # Input text area
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Paste or type text here...")
        layout.addWidget(self.input_text)
        
        # Upload button
        upload_btn = QPushButton('Upload Text File')
        upload_btn.clicked.connect(self.upload_file)
        layout.addWidget(upload_btn)
        
        # Summary length control
        length_label = QLabel('Summary Length:')
        layout.addWidget(length_label)
        
        self.summary_length = QSpinBox()
        self.summary_length.setRange(1, 100)
        self.summary_length.setValue(10)
        layout.addWidget(self.summary_length)
        
        # Generate summary button
        generate_btn = QPushButton('Generate Summary')
        generate_btn.clicked.connect(self.generate_summary)
        layout.addWidget(generate_btn)
        
        # Output text area
        self.summary_text = QTextEdit()
        self.summary_text.setPlaceholderText("Summary will appear here...")
        layout.addWidget(self.summary_text)
        
    def upload_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Upload Text File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r', encoding='utf-8') as file:
                self.input_text.setText(file.read())
    
    def generate_summary(self):
        text = self.input_text.toPlainText()
        if not text.strip():
            return
            
        # Text preprocessing
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Tokenize sentences
        sentences = sent_tokenize(text)
        
        # Calculate sentence scores
        scores = {}
        stop_words = set(stopwords.words('english'))
        
        for sentence in sentences:
            words = word_tokenize(sentence)
            word_count = len(words)
            if word_count > 0:
                scores[sentence] = word_count
        
        # Sort sentences by score
        sorted_sentences = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Generate summary
        summary_length = self.summary_length.value()
        summary_sentences = [sent[0] for sent in sorted_sentences[:summary_length]]
        summary = ' '.join(summary_sentences)
        
        self.summary_text.setText(summary)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TextSummarizer()
    ex.show()
    sys.exit(app.exec_())
