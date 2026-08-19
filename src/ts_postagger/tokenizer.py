"""Tokenization utilities."""

from dataclasses import dataclass
import re

from ts_tokenizer import CharFix, tokenize as ts_tokenize


_XML_TAG_LINE_RE = re.compile(
    r"""^<(?:
        /?[A-Za-z_][\w:.-]*
        (?:
            \s+[A-Za-z_:][\w:.-]*
            (?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s"'=<>]+))?
        )*
        \s*/?
        |
        \?[^<>]*\?
        |
        ![^<>]*
    )>$""",
    re.VERBOSE,
)


@dataclass(frozen=True, slots=True)
class TokenizerToken:
    text: str
    lower: str
    token_type: str


def _is_xml_tag_line(line: str) -> bool:
    return bool(_XML_TAG_LINE_RE.fullmatch(line.strip()))


def _token_from_tagged_line(line: str) -> TokenizerToken | None:
    if not line.strip() or "\t" not in line:
        return None

    surface, token_type = line.split("\t", 1)
    surface = surface.strip()
    token_type = token_type.strip()

    return TokenizerToken(
        text=surface,
        lower=CharFix.tr_lowercase(surface),
        token_type=token_type,
    )


def tokenize(text: str) -> list[TokenizerToken]:
    """
    Tokenize text with TS Tokenizer.
    """

    tokens: list[TokenizerToken] = []

    for input_line in text.splitlines():
        line = input_line.strip()
        if not line:
            continue

        if _is_xml_tag_line(line):
            tokens.append(
                TokenizerToken(
                    text=line,
                    lower=CharFix.tr_lowercase(line),
                    token_type="XML_Tag",
                )
            )
            continue

        tagged_output = ts_tokenize(input_line, "tagged")

        for tagged_line in tagged_output.splitlines():
            token = _token_from_tagged_line(tagged_line)
            if token is not None:
                tokens.append(token)

    return tokens
