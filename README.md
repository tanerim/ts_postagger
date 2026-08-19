# TS POSTagger

TS POSTagger is a Turkish part-of-speech tagging library with a hybrid pipeline:

1. [`ts-tokenizer`](https://pypi.org/project/ts-tokenizer/) tokenizes is used to tokenize input data.
2. A bundled spaCy POS model predicts tags. No external model download is required.

The package exposes:

- a Python API: `from ts_postagger import pos`
- a CLI: `ts-postagger`

## Installation

```bash
pip install ts-postagger
```

Requirements:

- Python `>=3.11`

The trained model is bundled with the package. No separate download step is required.

## Quick Start

```python
from ts_postagger import pos

tokens = pos("Defne'nin heyecanla beklediği #viyana yolculuğu bugün başladı.")

for token in tokens:
    print(token.text, token.pos)
```

Example output:

```text
Defne'nin   PropN
heyecanla   Adv
beklediği   Adj
#viyana     Hashtag
yolculuğu   Noun
bugün       Adv
başladı     Verb
.           Punc
```

## Python API

The main entrypoint is `pos(text: str) -> list[TSToken]`.

Each returned `TSToken` has these fields:

| Field | Description |
| --- | --- |
| `text` | Original surface form |
| `lower` | Turkish-aware lowercase form |
| `token_type` | Deterministic token class from [`ts-tokenizer`](https://pypi.org/project/ts-tokenizer/) |
| `tag` | Contextual grammatical prediction from the model |
| `pos` | Final output POS label |

`pos` is the field you should use as the final annotation.

### Minimal example

```python
from ts_postagger import pos

text = pos("Bugün yeni ve güzel bir gün!")

for token in text:
    print(token.pos)
```

### Convert results to dictionaries

`TSToken` is a dataclass, so standard dataclass helpers work:

```python
from dataclasses import asdict

from ts_postagger import pos

tokens = pos("#YeniBilgi yayımlandı.")
rows = [asdict(token) for token in tokens]

for row in rows:
    print(row)
```

Example dictionary:

```python
{
    "text": "#YeniBilgi",
    "lower": "#yenibilgi",
    "token_type": "Hashtag",
    "tag": "Noun",
    "pos": "Hashtag",
}
```

### Empty input

```python
from ts_postagger import pos

print(pos(""))
```

Output:

```python
[]
```

### Preserve XML lines for corpus output

XML tag lines are returned as structural tokens with `token_type`, `tag`, and
`pos` set to `"XML_Tag"`. Use `token.text` directly for those lines when writing
CWB-style corpus output:

```python
from ts_postagger import pos

tokens = pos('<text id="001" author="ts">\nBugün hava çok güzel.\n</text>')

for token in tokens:
    if token.token_type == "XML_Tag":
        print(token.text)
    else:
        print(f"{token.text}\t{token.lower}\t{token.pos}")
```

Output:

```text
<text id="001" author="ts">
Bugün	bugün	Adv
hava	hava	Noun
çok	çok	Adv
güzel	güzel	Adj
.	.	Punc
</text>
```

## Why `token_type`, `tag`, and `pos` are different

The library intentionally keeps multiple annotation layers.

For lexical tokens, the final output usually follows the POS model:

```text
çalışmalar  Valid_Word  Noun  Noun
yayımlandı  Valid_Word  Verb  Verb
```

For structural or social-media tokens, the final output stays deterministic even when the model predicts a regular grammatical tag:

```text
#YeniBilgi  Hashtag  Noun  Hashtag
@yeni  Mention  Noun  Mention
19.10.2026  Date  Num  Date
https://example.org  URL  Noun  URL
```

Meaning of each layer:

- `token_type`: deterministic label from the tokenizer
- `tag`: raw contextual prediction from the POS model
- `pos`: final POS output of TS POSTagger

## Turkish-aware lowercasing

The `lower` field uses Turkish-aware lowercasing from [`ts-tokenizer`](https://pypi.org/project/ts-tokenizer/).
This eliminates problems with Python's built-in lower() function errors.

```python
from ts_postagger import pos

tokens = pos("ISPARTA İSTANBUL")

for token in tokens:
    print(token.text, token.lower)
```

Output:

```text
Isparta  ısparta
İSTANBUL  istanbul
```

`lower` is a lowercase surface form. It is not a lemma.

## CLI

Installing the package also installs the `ts-postagger` command.

The CLI accepts either:

- a single positional text argument, or
- standard input

Default output format:

```text
TOKEN<TAB>POS
```

### Tag inline text

```bash
ts-postagger "Bugün yeni ve güzel bir gün!"
```

Example output:

```text
Bugün	Adv
yeni	Adj
ve	Conj
güzel	Adj
bir	Det
gün	Noun
!	Punc
```

### Lowercase only

```bash
ts-postagger -low "Bugün yeni ve güzel bir gün!"
```

Example output:

```text
bugün
yeni
ve
güzel
bir
gün
!
```

### Raw model tag

```bash
ts-postagger -tag "Bugün yeni ve güzel bir gün!"
```

Example output:

```text
Bugün	Adv
yeni	Adj
ve	Conj
güzel	Adj
bir	Det
gün	Noun
!	Punc
```

### Full output

```bash
ts-postagger -full "Bugün yeni ve güzel bir gün!"
```

Example output:

```text
Bugün	bugün	Adv
yeni	yeni	Adj
ve	ve	Conj
güzel	güzel	Adj
bir	bir	Det
gün	gün	Noun
!	!	Punc
```

Columns:

```text
TOKEN<TAB>LOWER<TAB>POS
```

### Read from stdin

```bash
echo "Bugün yeni ve güzel bir gün!" | ts-postagger
```

For a file, pass the file content through standard input:

```bash
ts-postagger -full < test_sentence.txt
```

The positional argument is interpreted as text, not as a file path.
XML tag lines are preserved as structural lines without POS columns, so CWB-style corpus markup can pass through the tagger:

```text
<text id="001" author="ts">
Bugün	bugün	Adv
</text>
```

### Run from a source checkout

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e .
ts-postagger -full < test_sentence.txt
```

You can also run the CLI module directly from the checkout:

```bash
python src/ts_postagger/cli.py -full < test_sentence.txt
```

### Version

```bash
ts-postagger -V
```

### Help

```bash
ts-postagger --help
```

## Notes

- The package name for installation is `ts-postagger`.
- The Python import package is `ts_postagger`.
- The CLI command is `ts-postagger`.

## Citation

If you use TS POSTagger in academic work, please cite the associated doctoral dissertation:

> Sezer, T. (2025). [*Dizilerden birimlere: Bilişimsel dilbilim çerçevesinde bir birimlendirici tasarımı*](https://tez.yok.gov.tr/UlusalTezMerkezi/TezGoster?key=Xau5rw3KuCgEuy-FuJQtsNVGSOOMCSQba2T5bZaDSDUTfOiTTVCpuBZPjDrUgB0i) [Doctoral dissertation, Hacettepe University].

## License

This project is licensed under the [MIT License](./LICENSE).
