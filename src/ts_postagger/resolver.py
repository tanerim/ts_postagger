"""Resolver helpers."""

# Tokenizer classes whose final label may be replaced
# by the contextual POS prediction.
POS_UPDATE_TYPES = frozenset({
    "Valid_Word",
    "Apostrophed",
    "OOV",
    "One_Char_Fixed",
})


def resolve_tag(token_type: str, predicted_pos: str) -> str:
    """
    Resolve the final hybrid tag.

    Lexically underspecified token classes receive the POS model output.
    Deterministic TS Tokenizer classes remain protected.
    """
    if token_type in POS_UPDATE_TYPES:
        return predicted_pos

    return token_type