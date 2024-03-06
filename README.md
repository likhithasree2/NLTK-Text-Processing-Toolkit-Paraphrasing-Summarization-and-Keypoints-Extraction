# NLTK-Text-Processing-Toolkit-Paraphrasing-Summarization-and-Keypoints-Extraction
NLTK Text Processing Tool: The Python application leverages the Natural Language Toolkit (NLTK) library to perform semantic text analysis tasks. It offers functionalities such as rephrasing sentences, generating summaries, and extracting key points from text.

## Features
- **Rephrasing:** Easily rephrase sentences to enhance clarity or variety in your text.
- **Summarization:** Generate concise summaries of longer texts for quick understanding.
- **Key Points Extraction:** Identify and extract important points from the text for easier comprehension.
  
## Libraries Used
- **NLTK (Natural Language Toolkit)(3.8.1):** NLTK is a powerful library for natural language processing tasks. It provides tools for tokenization, stemming, tagging, parsing, and semantic reasoning, among others.
- **PyQt5(5.15.9):** PyQt5 is a set of Python bindings for the Qt application framework. It is used here to create the graphical user interface (GUI) for the text processing tool.
- **Sumy(0.11.0):** Sumy is a Python library for automatic text summarization. It provides various algorithms for extracting key sentences from text documents.

## Code Explanation
- The main functionality of the application is divided into three parts: rephrasing, summarization, and generating important points from the input text.
- Rephrasing is done by finding synonyms for each word in the input text and selecting the most semantically similar synonym.
- Summarization is achieved using the TextRank algorithm implemented in the Sumy library, which ranks sentences based on their importance in the text.
- Generating important points involves identifying the most frequent words in the text and selecting sentences that contain those words, indicating their relevance.

## Installation
1. Clone this repository to your local machine.
2. Install the required dependencies by running `pip install <library name>`.
3. Run the application using Python with `nltk-text-tool.py`.

## Usage
1. Input your text in the provided text area.
2. Choose from the available options: "Rephrase", "Summarize", or "Important Points".
3. View the processed text in the output area.

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please fork the repository, make your changes, and submit a pull request.
