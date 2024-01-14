# memorywrapper

`MemoryWrapper` provides a slice-able front-end for a list of non-continuous memory backends, and only
 joins the needed area into a `bytes` object as needed.

It uses the new `__buffer__` protocol that is implementable in python starting with [python 3.12](https://docs.python.org/3.12/reference/datamodel.html?highlight=__buffer_#emulating-buffer-types).

## Installing

`pip install memorywrapper`

## Using

```py
    >>> from memorywrapper import MemoryWrapper
    >>> import struct
    >>> memory = MemoryWrapper([b"\x01\x02\x03", bytes([4,5,6])])
    >>> part = memory[1:-1]
    >>> (value,) = struct.unpack(">I", part)
    >>> f"0x{value:08x}"
    '0x02030405'
```

### make_slices

`make_slices` provides a way to cut something like bytes, memoryview, or memorywrapper into equal-sized chunks.

```py
    >>> from memorywrapper import make_slices
    >>> list(make_slices([1,2,3,4,5,6,7,8,9], 3))
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
```

