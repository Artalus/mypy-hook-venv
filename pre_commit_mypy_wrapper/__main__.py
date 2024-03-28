#!/usr/bin/env python

import os
import subprocess
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


CFG_NAME = '.pre-commit-mypy.yaml'


def main() -> int:
    # log(f'EXECUTABLE: {sys.executable}')
    # log(f'ARGV: {sys.argv}')
    # log('-'*10)
    script_name, *script_args = sys.argv
    if not script_args:
        log(f'USAGE: {script_name} <FILE> ...')
        sys.exit(1)

    config = Config.load_or_detect()

    if config.mypy is None:
        cmd = [config.python, '-m', 'mypy']
    else:
        cmd = [config.mypy]
        if config.python:
            cmd.extend(['--python-executable', config.python])
    cmd.extend(script_args)

    log('Will run:')
    log(f'Command: {cmd}')
    log(f'CWD: {os.getcwd()}\n\n')
    retcode = subprocess.call(cmd)
    return retcode


def log(*a, **kw):
    print('PCMW : ', *a, **kw, file=sys.stderr)


@dataclass
class Config:
    mypy: str | None = None
    python: str | None = None

    @staticmethod
    def load_or_detect() -> 'Config':
        cfg = Path(CFG_NAME)
        if cfg.is_file():
            with cfg.open() as f:
                loaded = yaml_load(f)
                config = Config(**loaded)

            for f in [config.mypy, config.python]:
                if f is not None and not Path(f).is_file():
                    log(f'ERROR: file `{f}` provided in config does not exist')
                    sys.exit(1)
        else:
            log(f'WARNING: path file {cfg.absolute()} is not present')
            config = Config(mypy=None, python=None)

        if config.mypy is None:
            if config.python is not None:
                log(f'`python` specified without `mypy` - using `{config.python} -m mypy`')
                return config
            if cfg.is_file():
                log('WARNING: path to `mypy` not specified in config')
            which = shutil.which('mypy')
            if not which:
                log(f'ERROR: `mypy` not available in PATH')
                sys.exit(1)

            log(
                f'Using `{which}` available in PATH as fallback.'
                f'\nConsider creating `{CFG_NAME}`, specifying paths to your `mypy` and/or `python`'
                ' executables.'
            )
            config.mypy = which

        return config


def yaml_load(file) -> dict[str, str]:
    """We have only a flat dict of strings, so no need to go full PyYaml"""
    line: str
    result = dict()
    for line in file:
        line, *comment = line.split('#', maxsplit=1)
        line = line.strip()
        if not line:
            continue
        key, value = line.split(': ', maxsplit=1)
        result[key] = value
    return result


if __name__ == '__main__':
    sys.exit(main())
