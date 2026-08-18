"""Tokenization utilities."""

from dataclasses import dataclass

from ts_tokenizer import CharFix, tokenize as ts_tokenize


@dataclass(frozen=True, slots=True)
class TokenizerToken:
    text: str
    lower: str
    token_type: str


def tokenize(text: str) -> list[TokenizerToken]:
    """
    Tokenize text with TS Tokenizer.
    """

    tokens: list[TokenizerToken] = []
    tagged_output = ts_tokenize(text, "tagged")

    for line in tagged_output.splitlines():
        if not line.strip():
            continue

        if "\t" not in line:
            continue

        surface, token_type = line.split("\t", 1)

        surface = surface.strip()
        token_type = token_type.strip()

        tokens.append(
            TokenizerToken(
                text=surface,
                lower=CharFix.tr_lowercase(surface),
                token_type=token_type,
            )
        )

    return tokens
