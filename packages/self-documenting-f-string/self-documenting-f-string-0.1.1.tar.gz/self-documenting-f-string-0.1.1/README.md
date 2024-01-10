# Self-documenting f-strings in Python 3.12

The current version of [pycodestyle](https://github.com/PyCQA/pycodestyle), and thus [flake8](https://github.com/PyCQA/flake8) doesn't see
to allow valid self-documenting f-strings anymore. They passed from Python 3.8 until now.
That's annoying, but I'm told it's on purpose, so here is a workaround that allows for the long time valid syntax to be used w/o ignoring
the errors globally or having to add a bunch of `# NoQA: blah...` all over your code. The best discussion I could find is found [here](https://github.com/PyCQA/pycodestyle/issues/1201). Comments were ignored and the discussion locked, thus this!

## Example

Here is and example of what used to be allowed:

```python
# example.py

var: int = 5
print(f'{var = }')

```

The versions used when this was discovered were:

```shell
✗ flake8 --version
7.0.0 (mccabe: 0.7.0, pycodestyle: 2.11.1, pyflakes: 3.2.0) CPython 3.12.1 on [Darwin | Linux]
```

Here are the new errors for the valid code:

```shell
✗ flake8 example.py
example.py:3:13: E251 unexpected spaces around keyword / parameter equals
example.py:3:15: E202 whitespace before '}'
example.py:3:15: E251 unexpected spaces around keyword / parameter equals
```
