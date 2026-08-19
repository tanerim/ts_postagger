"""Public API surface for the POS tagger."""

from pathlib import Path
from typing import Protocol

from .models import TSToken
from .predictor import POSPredictor
from .resolver import resolve_tag
from .tokenizer import tokenize


_DEFAULT_MODEL_PATH = Path(__file__).parent / "model"

_predictor: POSPredictor | None = None


class _TokenLike(Protocol):
    text: str


def _get_predictor() -> POSPredictor:
    global _predictor

    if _predictor is None:
        _predictor = POSPredictor(_DEFAULT_MODEL_PATH)

    return _predictor


def _is_model_token(token: _TokenLike) -> bool:
    return bool(token.text)


def pos(text: str) -> list[TSToken]:
    """
    Tokenize and annotate Turkish text.

    Pipeline:
        TS Tokenizer
            ↓
        contextual POS prediction over all tokens
            ↓
        deterministic hybrid resolver
    """

    tokenizer_tokens = tokenize(text)

    if not tokenizer_tokens:
        return []

    model_tokens = [
        token for token in tokenizer_tokens
        if token.token_type != "XML_Tag" and _is_model_token(token)
    ]
    predicted_tags = _get_predictor().predict([token.text for token in model_tokens])

    if len(predicted_tags) != len(model_tokens):
        raise RuntimeError(
            "Token alignment failure: "
            f"TS Tokenizer produced {len(model_tokens)} model tokens, "
            f"but POS tagger returned {len(predicted_tags)} predictions."
        )

    result: list[TSToken] = []
    predicted_tag_iter = iter(predicted_tags)

    for token in tokenizer_tokens:
        if token.token_type == "XML_Tag":
            result.append(
                TSToken(
                    text=token.text,
                    lower=token.lower,
                    token_type=token.token_type,
                    tag=token.token_type,
                    pos=token.token_type,
                )
            )
            continue

        if not _is_model_token(token):
            result.append(
                TSToken(
                    text=token.text,
                    lower=token.lower,
                    token_type=token.token_type,
                    tag=token.token_type,
                    pos=token.token_type,
                )
            )
            continue

        predicted_tag = next(predicted_tag_iter)
        final_pos = resolve_tag(
            token_type=token.token_type,
            predicted_pos=predicted_tag,
        )

        result.append(
            TSToken(
                text=token.text,
                lower=token.lower,
                token_type=token.token_type,
                tag=predicted_tag,
                pos=final_pos,
            )
        )

    return result


def tag(text: str) -> list[TSToken]:
    """Backward-compatible alias for pos()."""
    return pos(text)
