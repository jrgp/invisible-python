# invisible-python

Python source code, now with all the visible parts removed.
Each byte becomes eight bits, most significant bit first: a space for zero,
a tab for one. An `.ipy` file contains nothing else, not even newlines.
Files are eight times the size of the originals. Progress!

Requires Python 3.10 or newer. There are no runtime dependencies.

```sh
pip install -e .
echo 'print("hello from invisible python")' > hello.py
ipy encode hello.py
ipy run hello.ipy
ipy cat hello.ipy
ipy cat hello.ipy > restored.py
```

Use `ipy encode hello.py -o something.ipy` for a different output path.
Script arguments go after the filename: `ipy run hello.ipy foo bar`.
`python3 -m invisible_python` works in place of `ipy`.

Encode `secret_module.py`, then explicitly enable invisible imports:

```python
import invisible_python
invisible_python.install()
import secret_module
```

The hook finds `.ipy` modules on `sys.path`, including packages with
`__init__.ipy` and relative imports. Ordinary Python imports take priority;
remove or rename the original `.py` file to import its invisible counterpart.
Running an `.ipy` script enables the hook and adds its directory to the import path.

The codec also works directly on bytes:

```python
from invisible_python import encode, decode

encoded = encode(b'print("hello")\n')
assert decode(encoded) == b'print("hello")\n'
```

This is obfuscation, not encryption or security. Invisible code is still code:
only run or import files you trust.

To run the tests:

```sh
pip install -e '.[test]'
pytest
```
