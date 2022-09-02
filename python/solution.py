#!/usr/bin/env python3

from typing import (
    List,
    Union
)

from utils.image import (
    PackedImage,
    StrideImage,
)

from utils.pattern_remover import remove_all_patterns_from_image

from utils.function_tracer import FunctionTracer


# Tried distributing the computations using
# multiprocessing.Pool.map(callable, images)
# but the single-process performance was 3 times
# faster than the parallel one
def compute_solution(images: List[Union[PackedImage, StrideImage]]):
    ft = FunctionTracer("compute_solution", "seconds")

    for image in images:
        remove_all_patterns_from_image(image)

    del ft
