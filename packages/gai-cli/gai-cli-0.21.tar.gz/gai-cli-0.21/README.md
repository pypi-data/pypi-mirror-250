## Install Deps

```bash
sudo apt-get -qq install poppler-utils tesseract-ocr pandoc
pip install -q --user --upgrade pillow
pip install -q "unstructured[all-docs]"
pip install nltk
python -c "import nltk; nltk.download('punkt')"
python -c "import nltk; nltk.download('averaged_perceptron_tagger')"
```
