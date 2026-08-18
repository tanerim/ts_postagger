from pathlib import Path

import spacy
from spacy.tokens import Doc


class POSPredictor:
    def __init__(self, model_path: str | Path):
        self.nlp = spacy.load(model_path)

    def predict(self, words: list[str]) -> list[str]:
        if not words:
            return []

        doc = Doc(self.nlp.vocab, words=words)

        self.nlp.get_pipe("tok2vec")(doc)
        self.nlp.get_pipe("tagger")(doc)

        return [token.tag_ for token in doc]
