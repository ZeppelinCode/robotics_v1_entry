#!/usr/bin/env python3

from typing import Tuple
import string

EyePattern = Tuple[str, str, str, str, str]
BoolEyePattern = Tuple[Tuple[bool], Tuple[bool],
                       Tuple[bool], Tuple[bool], Tuple[bool]]

EYE_PATTERN_1: EyePattern = (
    "/---\\",
    "|   |",
    "|-o-|",
    "|   |",
    "\\---/"
)

EYE_PATTERN_2: EyePattern = (
    "/---\\",
    "| | |",
    "| 0 |",
    "| | |",
    "\\---/"
)

EYE_PATTERN_3: EyePattern = (
    "/---\\",
    "| | |",
    "|-q-|",
    "| | |",
    "\\---/"
)

EYE_PATTERN_4: EyePattern = (
    "/---\\",
    "|\\ /|",
    "| w |",
    "|/ \\|",
    "\\---/"
)


def __convert_str_eye_pattern_to_bool_pattern(
        s_pattern: EyePattern) -> BoolEyePattern:

    pattern = []
    for line in s_pattern:
        current_pattern_line = []
        pattern.append(current_pattern_line)
        for c in line:
            if c in string.whitespace:
                current_pattern_line.append(False)
            else:
                current_pattern_line.append(True)

    return pattern


BOOL_EYE_PATTERNS = tuple(__convert_str_eye_pattern_to_bool_pattern(p)
                          for p in [
    EYE_PATTERN_4,
    EYE_PATTERN_3,
    EYE_PATTERN_2,
    EYE_PATTERN_1,
])
