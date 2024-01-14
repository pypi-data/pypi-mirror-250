import re
import sys
from typing import Dict, cast

from typing_extensions import LiteralString

# https://github.com/pypa/twine/pull/551
if sys.version_info[:2] < (3, 9):  # coverage: exclude
    import importlib_resources
else:  # coverage: exclude
    import importlib.resources as importlib_resources

QUERIES_REGEX = re.compile(r"(?:\n|^)-- ([a-z0-9_]+) --\n(?:-- .+\n)*", re.MULTILINE)


def parse_query_file(query_file: str) -> Dict["str", LiteralString]:
    split = iter(QUERIES_REGEX.split(query_file))
    next(split)  # Consume the header of the file
    result = {}
    try:
        while True:
            key = next(split)
            value = next(split).strip()
            # procrastinate takes full responsibility for the queries, we
            # can safely vouch for them being as safe as if they were
            # defined in the code itself.
            result[key] = cast(LiteralString, value)
    except StopIteration:
        pass
    return result


def get_queries() -> Dict["str", LiteralString]:
    return parse_query_file(
        (importlib_resources.files("procrastinate.sql") / "queries.sql").read_text(
            encoding="utf-8"
        )
    )


queries = get_queries()
