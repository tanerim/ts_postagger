"""Model definitions."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TSToken:
    """
    Final TS POS Tagger token representation.

    text:
        Original surface form.

    lower:
        Turkish-safe lowercase surface form produced by
        ts-tokenizer CharFix.tr_lowercase().

    token_type:
        Deterministic lexical/structural class produced by TS Tokenizer.

    tag:
        Contextual grammatical prediction produced by the POS model.

    pos:
        Final hybrid POS annotation selected by the resolver.
    """

    text: str
    lower: str
    token_type: str
    tag: str
    pos: str
