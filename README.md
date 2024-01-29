This is a "proper" wrapper for `mypy` type checker to be used in `pre-commit`.

# How to use

Add the hook to your `.pre-commit-config.yaml`:
```yaml
repos:
- repo: https://github.com/Artalus/pre-commit-mypy
  rev: v0.1
  hooks:
  - id: mypy
```

Create file `.pre-commit-mypy.yaml`, specifying paths to the `mypy` executable you want to use,
or `python` executable you want it to work with through `--python-executable` flag:
```yaml
# .pre-commit-mypy.yaml
# if `mypy` is specified, `python` is not really necessary
mypy: D:\git\pre-commit-mypy\test\venv\Scripts\mypy.exe
python: D:\git\pre-commit-mypy\test\venv\Scripts\python.exe
```
On Windows, the path will be something like `d:/git/myproject/venv/Scripts/mypy.exe`.
On Linux - `/home/user/git/myproject/venv/bin/mypy`

Finally, add `.pre-commit-mypy.yaml` to your `.gitignore` - the path is local to your machine,
and will differ for your colleagues and CI machines.

Done. Now `pre-commit install`, break something, and try to commit it:
```
$ pre-commit run --all-files
mypy.....................................................................Failed
- hook id: mypy
- exit code: 1

PCMW :  Will run:
PCMW :  Command: ['D:\\git\\pre-commit-mypy\\test\\venv\\Scripts\\mypy.exe', 'test.py']
PCMW :  CWD: D:\git\pre-commit-mypy\test


test.py:11: error: Incompatible return value type (got "int", expected "Result[int, MyError]")  [return-value]
Found 1 error in 1 file (checked 1 source file)
```

# Why use this?

Using `pre-commit` + `mypy` + VS Code (and probably any other IDE as well) has 2 quirks:

1. `pre-commit` tends to install its hooks in a separate virtualenv.
Thus, `mypy` installed from the official `mirrors-mypy` hook repo will not know
anything about packages and their types used in your project's environment.
You need the hook to either launch your venv-specific `mypy` executable, or to
specify path to your `python` in your venv via `--python-executable` parameter.
Neither of these workarounds are really portalbe between OSes and developers.

2. VS Code specifically runs git commands without any notion of virtualenvs at all.
So even if you use `repo: local, entry: mypy` hook in your `.pre-commit-config.yaml`
as a workaround, `pre-commit` launched from Code will not know where this `mypy`
comes from in an arbitrary case.

The wrapper will read a user-provided path to their local `mypy` from a git-ignored
config file and will use it to check the files indicated by `pre-commit` executable.
If no config is provided, the wrapper will fallback to `mypy` executable present
in `PATH`, if any.
