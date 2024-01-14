from typing import Any, Generator, List


def generate_slices(limit: int, chunksize: int) -> List[slice]:
    cnt = (limit + chunksize - 1) // chunksize
    return [slice(idx * chunksize, (idx + 1) * chunksize) for idx in range(0, cnt)]


def make_slices[T: Any](something: T, chunksize: int) -> Generator[T, None, None]:
    """
    `make_slices` provides a way to cut something like bytes, memoryview, or memorywrapper into equal-sized chunks.

    >>> from memorywrapper import make_slices
    >>> list(make_slices([1,2,3,4,5,6,7,8,9], 3))
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    for slice in generate_slices(len(something), chunksize=chunksize):
        yield something[slice]
