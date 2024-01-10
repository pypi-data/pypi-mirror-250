import re
from collections.abc import Iterable

from anyerplint import util


class PreprocessError(Exception):
    """Raised by preprocessor"""


def tokenize(cont: str) -> list[str]:
    return re.split(r"([{}\"])", cont)


def walk_tokens(toks: list[str]) -> Iterable[tuple[str, int]]:
    depth = 0
    in_string = False
    escaping = False
    acc = []
    current_start_line = 0
    lnum = 1
    str_tok_start_index = None
    expr_start_index = 0
    diag_strings: list[str] = []
    for idx, tok in enumerate(toks):
        if not tok:
            # skip ''
            continue
        if depth > 0:
            acc.append(tok)

        match tok:
            case "{" if not in_string:
                depth += 1
                if depth == 1:
                    current_start_line = lnum
                    expr_start_index = idx
            case "}" if not in_string:
                depth -= 1
                if depth == 0:
                    # pop already pushed }
                    acc.pop()
                    yield ("".join(acc), current_start_line)
                    diag_strings = []
                    acc = []
            case '"' if not escaping and depth > 0:
                in_string = not in_string
                if in_string:
                    str_tok_start_index = idx
                else:
                    diag_strings.append("".join(toks[str_tok_start_index : idx + 1]))
            case _:
                ending_quote_count = util.count_trailing(tok, "\\")
                escaping = ending_quote_count % 2 != 0

        lnum += tok.count("\n")

    if depth > 0:
        raise PreprocessError(
            f"Unterminated expression (too many {{ characters) at {current_start_line}. Starting with: "
            + repr("".join(toks[expr_start_index : expr_start_index + 10]))
        )
    if in_string:
        stringlist = " :: ".join(repr(s)[:500] for s in diag_strings[:100])
        raise PreprocessError(
            f"Unterminated string in expressions, line {current_start_line}. All strings: "
            + stringlist[:2000]
        )


def get_expressions(cont: str) -> list[tuple[str, int]]:
    tokens = tokenize(cont)
    return list(walk_tokens(tokens))
